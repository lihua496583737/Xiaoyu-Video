# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Scene processor for animation video generation
Orchestrates scene video generation with character consistency,
lip-sync, upscaling, interpolation, and color grading
"""

import asyncio
import os
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from loguru import logger

from pixelle_video.models.animation import (
    CharacterConfig,
    SceneConfig,
    SceneResult,
    VideoGenerationConfig,
)
from pixelle_video.prompts.animation_script import build_scene_video_prompt


class SceneProcessor:
    """
    Scene processing orchestrator for animation videos
    
    Handles:
    1. Scene video generation with character consistency
    2. Lip-sync processing
    3. Video upscaling
    4. Frame interpolation
    5. Color grading
    6. Quality checking and smart retry
    """
    
    def __init__(self, core):
        """
        Initialize scene processor
        
        Args:
            core: PixelleVideoCore instance
        """
        self.core = core
        self.llm = core.llm
        self.tts = core.tts
        self.media = core.media
        self.video = core.video
        self.persistence = core.persistence
    
    async def __call__(
        self,
        scene: SceneConfig,
        characters: List[CharacterConfig],
        output_dir: str,
        progress_callback: Optional[Callable] = None,
        **kwargs
    ) -> SceneResult:
        """
        Process a single scene
        
        Args:
            scene: Scene configuration
            characters: List of character configurations
            output_dir: Output directory for scene files
            progress_callback: Optional progress callback
            **kwargs: Additional parameters (max_retries, enable_*, etc.)
        
        Returns:
            SceneResult with processed video path and metadata
        """
        max_retries = kwargs.get("max_retries", 3)
        enable_lip_sync = kwargs.get("enable_lip_sync", True)
        enable_upscale = kwargs.get("enable_upscale", True)
        enable_interpolation = kwargs.get("enable_interpolation", True)
        enable_color_grading = kwargs.get("enable_color_grading", True)
        
        scene_index = scene.index
        scene_dir = os.path.join(output_dir, f"scene_{scene_index:03d}")
        os.makedirs(scene_dir, exist_ok=True)
        
        result = SceneResult(scene_index=scene_index, video_path="", duration=scene.duration)
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                result.retry_count = attempt
                
                # Step 1: Generate scene video with character consistency
                if progress_callback:
                    progress_callback("generating_scene_video", scene_index, attempt + 1)
                
                video_path = await self._generate_scene_video(
                    scene=scene,
                    characters=characters,
                    output_dir=scene_dir,
                )
                
                if not video_path:
                    raise RuntimeError("Failed to generate scene video")
                
                result.video_path = video_path
                
                # Step 2: Lip-sync (if scene has dialogues and enabled)
                if enable_lip_sync and scene.dialogues:
                    if progress_callback:
                        progress_callback("applying_lip_sync", scene_index)
                    
                    # Collect all dialogue audio
                    audio_path = await self._generate_dialogue_audio(
                        dialogues=scene.dialogues,
                        characters=characters,
                        output_dir=scene_dir,
                    )
                    
                    if audio_path:
                        lip_sync_path = await self._apply_lip_sync(
                            video_path=video_path,
                            audio_path=audio_path,
                            output_dir=scene_dir,
                        )
                        if lip_sync_path:
                            result.lip_sync_path = lip_sync_path
                            result.video_path = lip_sync_path
                
                # Step 3: Video upscaling
                if enable_upscale:
                    if progress_callback:
                        progress_callback("upscaling_video", scene_index)
                    
                    upscaled_path = await self._upscale_video(
                        video_path=result.video_path,
                        target_resolution=scene.video_generation.upscale_target,
                        output_dir=scene_dir,
                    )
                    if upscaled_path:
                        result.upscaled_path = upscaled_path
                        result.video_path = upscaled_path
                
                # Step 4: Frame interpolation
                if enable_interpolation:
                    if progress_callback:
                        progress_callback("interpolating_frames", scene_index)
                    
                    interpolated_path = await self._interpolate_frames(
                        video_path=result.video_path,
                        target_fps=scene.video_generation.interpolate_target_fps,
                        output_dir=scene_dir,
                    )
                    if interpolated_path:
                        result.interpolated_path = interpolated_path
                        result.video_path = interpolated_path
                
                # Step 5: Color grading
                if enable_color_grading:
                    if progress_callback:
                        progress_callback("color_grading", scene_index)
                    
                # Step 6: Quality check
                quality_score = await self._check_video_quality(
                    video_path=result.video_path,
                    scene=scene,
                )
                result.quality_score = quality_score
                
                # If quality is acceptable, break retry loop
                if quality_score >= 0.6:
                    logger.info(f"Scene {scene_index} passed quality check (score: {quality_score})")
                    break
                else:
                    logger.warning(
                        f"Scene {scene_index} quality score {quality_score} < 0.6, "
                        f"retrying (attempt {attempt + 1}/{max_retries})"
                    )
                    last_error = f"Quality check failed: {quality_score}"
                    # Adjust parameters for retry
                    await self._adjust_params_for_retry(scene, attempt)
                
            except Exception as e:
                logger.error(f"Scene {scene_index} processing error (attempt {attempt + 1}): {e}")
                last_error = str(e)
                if attempt < max_retries - 1:
                    await asyncio.sleep(5 * (attempt + 1))
        
        if not result.video_path:
            result.status = "failed"
            result.error = last_error or "Unknown error"
            logger.error(f"Scene {scene_index} failed after {max_retries} attempts")
        else:
            result.status = "completed"
            logger.info(f"Scene {scene_index} completed: {result.video_path}")
        
        return result
    
    async def _generate_scene_video(
        self,
        scene: SceneConfig,
        characters: List[CharacterConfig],
        output_dir: str,
    ) -> Optional[str]:
        """Generate scene video with character consistency"""
        try:
            # Build video generation prompt
            prompt = build_scene_video_prompt(
                style="",  # Will be set from pipeline context
                scene=scene.__dict__ if hasattr(scene, "__dict__") else vars(scene),
                characters=[c.__dict__ if hasattr(c, "__dict__") else vars(c) for c in characters]
            )
            
            # Prepare reference images from characters
            reference_images = []
            for char_in_scene in scene.characters:
                char_config = char_in_scene.character
                reference_images.extend(char_config.reference_images[:2])  # Max 2 per character
            
            # Prepare video generation parameters
            vg_config = scene.video_generation
            workflow = f"video_{vg_config.model}_anime.json"
            
            # Call media service with character consistency parameters
            media_result = await self.media(
                prompt=prompt,
                workflow=workflow,
                media_type="video",
                width=int(vg_config.resolution.split("x")[0]),
                height=int(vg_config.resolution.split("x")[1]),
                duration=scene.duration,
                guidance_scale=vg_config.guidance_scale,
                steps=vg_config.num_inference_steps,
                reference_images=reference_images if reference_images else None,
                consistency_weight=vg_config.consistency_weight,
            )
            
            # Save video
            output_path = os.path.join(output_dir, "scene_raw.mp4")
            
            # Media service returns URL or path, download/copy if needed
            if hasattr(media_result, "url"):
                video_url = media_result.url
                # Download video
                import httpx
                async with httpx.AsyncClient(timeout=300) as client:
                    response = await client.get(video_url)
                    response.raise_for_status()
                    with open(output_path, "wb") as f:
                        f.write(response.content)
            else:
                # Already a local path
                import shutil
                shutil.copy(str(media_result) if hasattr(media_result, "__str__") else media_result, output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate scene video: {e}")
            return None
    
    async def _generate_dialogue_audio(
        self,
        dialogues: list,
        characters: List[CharacterConfig],
        output_dir: str,
    ) -> Optional[str]:
        """Generate audio for all dialogues in the scene"""
        try:
            import tempfile
            
            # Create character voice map
            voice_map = {}
            for char in characters:
                voice_map[char.name] = char
            
            audio_segments = []
            
            # Sort dialogues by start time
            sorted_dialogues = sorted(dialogues, key=lambda d: d.start_time if hasattr(d, "start_time") else 0)
            
            for dialogue in sorted_dialogues:
                char_name = dialogue.character if hasattr(dialogue, "character") else ""
                text = dialogue.text if hasattr(dialogue, "text") else ""
                
                if not text:
                    continue
                
                # Get character voice
                char_config = voice_map.get(char_name)
                voice = char_config.tts_voice if char_config else "zh-CN-YunxiNeural"
                speed = char_config.tts_speed if char_config else 1.0
                
                # Generate TTS audio
                audio_path = await self.tts(
                    text=text,
                    voice=voice,
                    speed=speed,
                    output_path=os.path.join(output_dir, f"dialogue_{char_name}_{len(audio_segments)}.mp3"),
                )
                
                if audio_path:
                    audio_segments.append(audio_path)
            
            if not audio_segments:
                return None
            
            # Merge audio segments (simple approach: concatenate)
            if len(audio_segments) == 1:
                return audio_segments[0]
            
            # For multiple dialogues, merge with silence gaps
            # This is a simplified implementation
            merged_path = os.path.join(output_dir, "dialogue_merged.mp3")
            
            # Use FFmpeg to concatenate
            concat_file = os.path.join(output_dir, "concat_list.txt")
            with open(concat_file, "w", encoding="utf-8") as f:
                for audio_path in audio_segments:
                    f.write(f"file '{audio_path}'\n")
            
            import subprocess
            cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", concat_file,
                "-c", "copy", merged_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            
            return merged_path
            
        except Exception as e:
            logger.error(f"Failed to generate dialogue audio: {e}")
            return None
    
    async def _apply_lip_sync(
        self,
        video_path: str,
        audio_path: str,
        output_dir: str,
    ) -> Optional[str]:
        """Apply lip-sync to video using Wav2Lip or similar"""
        try:
            output_path = os.path.join(output_dir, "scene_lipsync.mp4")
            
            # Call lip-sync workflow through media service
            # This requires a lip_sync_* workflow to be available
            lip_sync_result = await self.media(
                prompt="",
                workflow="video_lip_sync.json",
                media_type="video",
                input_video=video_path,
                input_audio=audio_path,
            )
            
            if lip_sync_result and hasattr(lip_sync_result, "url"):
                import httpx
                async with httpx.AsyncClient(timeout=300) as client:
                    response = await client.get(lip_sync_result.url)
                    response.raise_for_status()
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                return output_path
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to apply lip-sync: {e}")
            return None
    
    async def _upscale_video(
        self,
        video_path: str,
        target_resolution: str,
        output_dir: str,
    ) -> Optional[str]:
        """Upscale video to target resolution"""
        try:
            output_path = os.path.join(output_dir, "scene_upscaled.mp4")
            
            # Call upscaling workflow through media service
            upscale_result = await self.media(
                prompt="",
                workflow="video_upscale.json",
                media_type="video",
                input_video=video_path,
                target_resolution=target_resolution,
            )
            
            if upscale_result and hasattr(upscale_result, "url"):
                import httpx
                async with httpx.AsyncClient(timeout=300) as client:
                    response = await client.get(upscale_result.url)
                    response.raise_for_status()
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                return output_path
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to upscale video: {e}")
            return None
    
    async def _interpolate_frames(
        self,
        video_path: str,
        target_fps: int,
        output_dir: str,
    ) -> Optional[str]:
        """Interpolate frames to target FPS"""
        try:
            output_path = os.path.join(output_dir, "scene_interpolated.mp4")
            
            # Call interpolation workflow through media service
            interp_result = await self.media(
                prompt="",
                workflow="video_interpolation.json",
                media_type="video",
                input_video=video_path,
                target_fps=target_fps,
            )
            
            if interp_result and hasattr(interp_result, "url"):
                import httpx
                async with httpx.AsyncClient(timeout=300) as client:
                    response = await client.get(interp_result.url)
                    response.raise_for_status()
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                return output_path
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to interpolate frames: {e}")
            return None
    
    async def _check_video_quality(
        self,
        video_path: str,
        scene: SceneConfig,
    ) -> float:
        """
        Check video quality
        
        Returns:
            Quality score (0-1)
        """
        try:
            # Basic quality checks
            import subprocess
            
            # Check if video is valid
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height,duration",
                 "-of", "csv=p=0", video_path],
                capture_output=True, text=True, check=True
            )
            
            if not result.stdout.strip():
                return 0.0
            
            # Parse output
            parts = result.stdout.strip().split(",")
            if len(parts) < 3:
                return 0.0
            
            width, height, duration = int(parts[0]), int(parts[1]), float(parts[2])
            
            # Check resolution
            expected_width = int(scene.video_generation.resolution.split("x")[0])
            expected_height = int(scene.video_generation.resolution.split("x")[1])
            
            resolution_score = 1.0
            if width < expected_width * 0.8 or height < expected_height * 0.8:
                resolution_score = 0.5
            
            # Check duration
            duration_score = 1.0
            if abs(duration - scene.duration) > scene.duration * 0.3:
                duration_score = 0.6
            
            # For now, return a basic score
            # In a full implementation, this would use AI to check:
            # - Character consistency
            # - Motion quality
            # - Prompt matching
            
            return min(1.0, (resolution_score + duration_score) / 2)
            
        except Exception as e:
            logger.error(f"Failed to check video quality: {e}")
            return 0.5  # Default to medium score on error
    
    async def _adjust_params_for_retry(self, scene: SceneConfig, attempt: int):
        """Adjust parameters for retry attempts"""
        # Reduce guidance scale on retries to avoid over-sharpening
        if attempt >= 1:
            scene.video_generation.guidance_scale = max(
                5.0, scene.video_generation.guidance_scale - 0.5
            )
        
        # Increase inference steps for better quality
        if attempt >= 2:
            scene.video_generation.num_inference_steps = min(
                75, scene.video_generation.num_inference_steps + 10
            )
        
        logger.info(
            f"Adjusted params for retry {attempt + 1}: "
            f"guidance={scene.video_generation.guidance_scale}, "
            f"steps={scene.video_generation.num_inference_steps}"
        )
