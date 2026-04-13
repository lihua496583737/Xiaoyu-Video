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
Animation video generation pipeline
Generates high-quality animation videos with character consistency,
lip-sync, cinematic camera, and special effects
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from loguru import logger

from pixelle_video.models.animation import (
    AnimationScript,
    CharacterConfig,
    SceneConfig,
    VideoGenerationConfig,
)
from pixelle_video.models.progress import ProgressEvent
from pixelle_video.models.storyboard import (
    Storyboard,
    StoryboardConfig,
    StoryboardFrame,
    VideoGenerationResult,
)
from pixelle_video.pipelines.linear import LinearVideoPipeline, PipelineContext
from pixelle_video.prompts.animation_script import (
    ANIMATION_SCRIPT_PROMPT,
    ANIMATION_STYLE_PROMPTS,
)
from pixelle_video.services.scene_processor import SceneProcessor


class AnimationPipeline(LinearVideoPipeline):
    """
    High-quality animation video generation pipeline
    
    Generates animation videos with:
    - Character consistency (IP-Adapter FaceID)
    - Lip-sync for dialogues
    - Cinematic camera movements
    - Special effects (magic, weather, particles)
    - Post-processing (upscaling, interpolation, color grading)
    """
    
    def __init__(self, pixelle_video_core):
        super().__init__(pixelle_video_core)
        self.scene_processor = SceneProcessor(pixelle_video_core)
    
    async def setup_environment(self, ctx: PipelineContext):
        """Set up task environment"""
        # Call parent setup
        await super().setup_environment(ctx)
        
        # Extract animation-specific parameters
        ctx.params.setdefault("animation_style", "fanren_xianxia")
        ctx.params.setdefault("video_model", "ltx2.3")
        ctx.params.setdefault("max_retries", 3)
        ctx.params.setdefault("fail_fast", False)
        ctx.params.setdefault("enable_upscale", True)
        ctx.params.setdefault("enable_interpolation", True)
        ctx.params.setdefault("enable_color_grading", True)
        ctx.params.setdefault("enable_lip_sync", True)
        ctx.params.setdefault("n_scenes", 5)
        ctx.params.setdefault("target_duration", 30.0)
        
        logger.info(f"Animation pipeline initialized: style={ctx.params['animation_style']}, model={ctx.params['video_model']}")
    
    async def generate_content(self, ctx: PipelineContext):
        """Generate animation script using LLM"""
        self._report_progress(
            ctx.progress_callback, "generating_script", 0.05,
            extra_info="正在生成动画脚本..."
        )
        
        # Get parameters
        topic = ctx.input_text
        style = ctx.params.get("animation_style", "fanren_xianxia")
        n_scenes = ctx.params.get("n_scenes", 5)
        target_duration = ctx.params.get("target_duration", 30.0)
        
        # Get style config
        style_config = ANIMATION_STYLE_PROMPTS.get(style, {})
        style_name = style_config.get("name_en", style)
        
        # Build prompt
        prompt = ANIMATION_SCRIPT_PROMPT.format(
            topic=topic,
            style=style_name,
            characters="User will define characters separately",
            duration=target_duration,
            n_scenes=n_scenes,
        )
        
        # Call LLM to generate script
        try:
            script_json = await self.llm(
                prompt=prompt,
                model=self.core.config.llm.model,
                temperature=0.7,
                max_tokens=4000,
            )
            
            # Parse JSON response
            # Remove markdown code blocks if present
            if "```json" in script_json:
                script_json = script_json.split("```json")[1].split("```")[0].strip()
            elif "```" in script_json:
                script_json = script_json.split("```")[1].split("```")[0].strip()
            
            script_data = json.loads(script_json)
            
            # Store script in context
            ctx.params["animation_script_data"] = script_data
            
            # Extract title
            ctx.title = script_data.get("title", topic)
            
            # Store characters
            characters_data = script_data.get("characters", [])
            ctx.params["animation_characters"] = characters_data
            
            # Store scenes
            scenes_data = script_data.get("scenes", [])
            ctx.params["animation_scenes"] = scenes_data
            
            logger.info(f"Animation script generated: {len(scenes_data)} scenes, title={ctx.title}")
            
            self._report_progress(
                ctx.progress_callback, "script_completed", 0.10,
                extra_info=f"动画脚本生成完成: {len(scenes_data)} 个场景"
            )
            
        except Exception as e:
            logger.error(f"Failed to generate animation script: {e}")
            raise RuntimeError(f"LLM script generation failed: {e}")
    
    async def determine_title(self, ctx: PipelineContext):
        """Title already determined in generate_content"""
        if not ctx.title:
            ctx.title = ctx.input_text[:50]
    
    async def plan_visuals(self, ctx: PipelineContext):
        """Plan visuals - prepare character reference images"""
        characters_data = ctx.params.get("animation_characters", [])
        
        if not characters_data:
            logger.warning("No characters defined, generating with default settings")
            return
        
        self._report_progress(
            ctx.progress_callback, "generating_character_refs", 0.15,
            extra_info=f"准备 {len(characters_data)} 个角色参考图..."
        )
        
        # For each character, generate reference images if not provided
        for i, char_data in enumerate(characters_data):
            ref_images = char_data.get("reference_images", [])
            
            if not ref_images:
                # Generate character reference image
                self._report_progress(
                    ctx.progress_callback, "generating_character_ref",
                    0.15 + (i / max(1, len(characters_data))) * 0.10,
                    frame_current=i + 1,
                    frame_total=len(characters_data),
                    extra_info=f"生成角色参考图: {char_data.get('name', f'角色{i+1}')}"
                )
                
                # Build character appearance prompt
                appearance = char_data.get("appearance", {})
                clothing = char_data.get("clothing", {})
                
                char_prompt = f"Character design sheet, front view, {appearance.get('gender', '')} {appearance.get('age_range', '')}, "
                char_prompt += f"{appearance.get('hair', '')}, {appearance.get('face', '')}, "
                char_prompt += f"wearing {clothing.get('outfit', '')}, "
                char_prompt += f"{clothing.get('accessories', '')}, "
                char_prompt += "character design, clean background, high quality"
                
                # Generate reference image
                try:
                    style = ctx.params.get("animation_style", "fanren_xianxia")
                    style_config = ANIMATION_STYLE_PROMPTS.get(style, {})
                    full_prompt = f"{style_config.get('style_prefix', '')}, {char_prompt}"
                    
                    image_result = await self.media(
                        prompt=full_prompt,
                        media_type="image",
                        width=512,
                        height=768,
                    )
                    
                    if image_result:
                        # Store image path in character data
                        image_path = str(getattr(image_result, "url", image_result))
                        char_data["reference_images"] = [image_path]
                        logger.info(f"Generated reference image for {char_data.get('name')}")
                except Exception as e:
                    logger.warning(f"Failed to generate reference image for {char_data.get('name')}: {e}")
        
        self._report_progress(
            ctx.progress_callback, "character_refs_completed", 0.25,
            extra_info="角色参考图准备完成"
        )
    
    async def initialize_storyboard(self, ctx: PipelineContext):
        """Initialize storyboard with animation scenes"""
        scenes_data = ctx.params.get("animation_scenes", [])
        characters_data = ctx.params.get("animation_characters", [])
        
        if not scenes_data:
            raise RuntimeError("No scenes available for animation")
        
        # Create storyboard config
        style = ctx.params.get("animation_style", "fanren_xianxia")
        style_config = ANIMATION_STYLE_PROMPTS.get(style, {})
        video_model = ctx.params.get("video_model", "ltx2.3")
        
        config = StoryboardConfig(
            media_width=720,
            media_height=1280,
            task_id=ctx.task_id,
            n_storyboard=len(scenes_data),
            video_fps=24,
            tts_inference_mode="local",
            animation_style=style,
            video_model=video_model,
            max_retries=ctx.params.get("max_retries", 3),
            fail_fast=ctx.params.get("fail_fast", False),
            enable_upscale=ctx.params.get("enable_upscale", True),
            enable_interpolation=ctx.params.get("enable_interpolation", True),
            enable_color_grading=ctx.params.get("enable_color_grading", True),
            enable_lip_sync=ctx.params.get("enable_lip_sync", True),
            prompt_prefix=style_config.get("style_prefix", ""),
        )
        
        # Create frames (one per scene)
        frames = []
        for i, scene_data in enumerate(scenes_data):
            frame = StoryboardFrame(
                index=i,
                narration=" ".join([d.get("text", "") for d in scene_data.get("dialogues", [])]),
                image_prompt="",  # Will be built during scene processing
                scene_config=scene_data,
                status="pending",
            )
            frames.append(frame)
        
        # Create storyboard
        ctx.storyboard = Storyboard(
            title=ctx.title,
            config=config,
            frames=frames,
            total_duration=sum(scene_data.get("duration", 5.0) for scene_data in scenes_data),
        )
        
        logger.info(f"Storyboard initialized: {len(frames)} scenes")
    
    async def produce_assets(self, ctx: PipelineContext):
        """Produce assets - generate scene videos (core step)"""
        scenes_data = ctx.params.get("animation_scenes", [])
        characters_data = ctx.params.get("animation_characters", [])
        
        if not scenes_data:
            raise RuntimeError("No scenes to process")
        
        # Convert character data to CharacterConfig objects
        characters = []
        for char_data in characters_data:
            char_config = CharacterConfig(
                name=char_data.get("name", "Unknown"),
                description=char_data.get("description", ""),
                reference_images=char_data.get("reference_images", []),
                tts_voice=char_data.get("tts_voice", "zh-CN-YunxiNeural"),
            )
            characters.append(char_config)
        
        # Process scenes
        max_retries = ctx.params.get("max_retries", 3)
        enable_lip_sync = ctx.params.get("enable_lip_sync", True)
        enable_upscale = ctx.params.get("enable_upscale", True)
        enable_interpolation = ctx.params.get("enable_interpolation", True)
        enable_color_grading = ctx.params.get("enable_color_grading", True)
        
        # Check if we can process scenes in parallel (RunningHub with concurrency)
        use_parallel = ctx.params.get("use_parallel", False)
        
        if use_parallel:
            # Parallel processing with semaphore
            semaphore = asyncio.Semaphore(ctx.params.get("concurrent_limit", 3))
            
            async def process_scene_with_semaphore(i, scene_data):
                async with semaphore:
                    return await self._process_single_scene(
                        scene_index=i,
                        scene_data=scene_data,
                        characters=characters,
                        ctx=ctx,
                        max_retries=max_retries,
                        enable_lip_sync=enable_lip_sync,
                        enable_upscale=enable_upscale,
                        enable_interpolation=enable_interpolation,
                        enable_color_grading=enable_color_grading,
                    )
            
            tasks = [process_scene_with_semaphore(i, sd) for i, sd in enumerate(scenes_data)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update frames with results
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Scene {i} failed: {result}")
                    ctx.frames[i].status = "failed"
                    ctx.frames[i].error = str(result)
                elif result:
                    ctx.frames[i].video_segment_path = result.video_path
                    ctx.frames[i].quality_score = result.quality_score
                    ctx.frames[i].status = result.status
                    ctx.frames[i].duration = result.duration
        else:
            # Sequential processing
            for i, scene_data in enumerate(scenes_data):
                result = await self._process_single_scene(
                    scene_index=i,
                    scene_data=scene_data,
                    characters=characters,
                    ctx=ctx,
                    max_retries=max_retries,
                    enable_lip_sync=enable_lip_sync,
                    enable_upscale=enable_upscale,
                    enable_interpolation=enable_interpolation,
                    enable_color_grading=enable_color_grading,
                )
                
                if result:
                    ctx.frames[i].video_segment_path = result.video_path
                    ctx.frames[i].quality_score = result.quality_score
                    ctx.frames[i].status = result.status
                    ctx.frames[i].duration = result.duration
                    ctx.frames[i].error = result.error if result.status == "failed" else None
                else:
                    ctx.frames[i].status = "failed"
                    ctx.frames[i].error = "Processing returned None"
                
                # Check fail_fast
                if ctx.params.get("fail_fast", False) and ctx.frames[i].status == "failed":
                    raise RuntimeError(f"Scene {i} failed and fail_fast is enabled")
    
    async def _process_single_scene(
        self,
        scene_index: int,
        scene_data: dict,
        characters: list,
        ctx: PipelineContext,
        max_retries: int,
        enable_lip_sync: bool,
        enable_upscale: bool,
        enable_interpolation: bool,
        enable_color_grading: bool,
    ):
        """Process a single scene"""
        # Build SceneConfig from scene_data
        scene_config = self._build_scene_config(scene_index, scene_data)
        
        # Create scene output directory
        scene_output_dir = os.path.join(ctx.task_dir, "scenes", f"scene_{scene_index:03d}")
        os.makedirs(scene_output_dir, exist_ok=True)
        
        # Progress callback
        def scene_progress(event_type, current_idx, attempt=None):
            base_progress = 0.25
            scene_weight = 0.55  # Scenes take 55% of total time
            per_scene_progress = scene_weight / max(1, len(ctx.frames))
            
            progress = base_progress + (scene_index / max(1, len(ctx.frames))) * scene_weight
            
            extra = f"场景 {scene_index + 1}/{len(ctx.frames)}"
            if attempt:
                extra += f" (尝试 {attempt})"
            
            self._report_progress(
                ctx.progress_callback,
                event_type,
                progress,
                frame_current=scene_index + 1,
                frame_total=len(ctx.frames),
                extra_info=extra,
            )
        
        # Process scene
        result = await self.scene_processor(
            scene=scene_config,
            characters=characters,
            output_dir=scene_output_dir,
            progress_callback=scene_progress,
            max_retries=max_retries,
            enable_lip_sync=enable_lip_sync,
            enable_upscale=enable_upscale,
            enable_interpolation=enable_interpolation,
            enable_color_grading=enable_color_grading,
        )
        
        return result
    
    def _build_scene_config(self, scene_index: int, scene_data: dict) -> SceneConfig:
        """Build SceneConfig from scene data dict"""
        # Build video generation config
        vg_data = scene_data.get("video_generation", {})
        vg_config = VideoGenerationConfig(
            model=vg_data.get("model", "ltx2.3"),
            resolution=vg_data.get("resolution", "720x1280"),
            fps=vg_data.get("fps", 24),
            guidance_scale=vg_data.get("guidance_scale", 7.0),
            num_inference_steps=vg_data.get("num_inference_steps", 50),
        )
        
        # Build camera config
        camera_data = scene_data.get("camera", {})
        from pixelle_video.models.animation import CameraSetup
        camera_config = CameraSetup(
            shot_type=camera_data.get("shot_type", "medium_shot"),
            movement=camera_data.get("movement", "static"),
            movement_params=camera_data.get("movement_params", {}),
            focus=camera_data.get("focus", "character"),
            focus_pull=camera_data.get("focus_pull", False),
        )
        
        # Build effects
        from pixelle_video.models.animation import Effect
        effects = []
        for fx_data in scene_data.get("effects", []):
            effects.append(Effect(
                effect_type=fx_data.get("effect_type", "magic"),
                effect_name=fx_data.get("effect_name", ""),
                start_time=fx_data.get("start_time", 0.0),
                duration=fx_data.get("duration", 1.0),
                intensity=fx_data.get("intensity", 1.0),
                color=fx_data.get("color"),
                description=fx_data.get("description", ""),
            ))
        
        # Build dialogues
        from pixelle_video.models.animation import Dialogue
        dialogues = []
        for dlg_data in scene_data.get("dialogues", []):
            dialogues.append(Dialogue(
                character=dlg_data.get("character", ""),
                text=dlg_data.get("text", ""),
                emotion=dlg_data.get("emotion", "neutral"),
                start_time=dlg_data.get("start_time", 0.0),
                end_time=dlg_data.get("end_time", 2.0),
            ))
        
        # Build characters in scene
        from pixelle_video.models.animation import CharacterInScene
        characters_in_scene = []
        for char_data in scene_data.get("characters", []):
            # Create a minimal CharacterConfig for the scene
            char_config = CharacterConfig(
                name=char_data.get("character", ""),
                description="",
            )
            characters_in_scene.append(CharacterInScene(
                character=char_config,
                position=char_data.get("position", "center"),
                initial_expression=char_data.get("initial_expression", "neutral"),
                initial_pose=char_data.get("initial_pose", "idle"),
            ))
        
        # Create SceneConfig
        scene_config = SceneConfig(
            index=scene_index,
            description=scene_data.get("description", ""),
            background=scene_data.get("background", ""),
            time_of_day=scene_data.get("time_of_day", "day"),
            weather=scene_data.get("weather", "clear"),
            characters=characters_in_scene,
            action_description=scene_data.get("action_description", ""),
            dialogues=dialogues,
            camera=camera_config,
            effects=effects,
            duration=scene_data.get("duration", 5.0),
            video_generation=vg_config,
        )
        
        return scene_config
    
    async def post_production(self, ctx: PipelineContext):
        """Post-production: concatenate scenes, add audio, BGM"""
        self._report_progress(
            ctx.progress_callback, "concatenating_scenes", 0.85,
            extra_info="正在拼接场景..."
        )
        
        # Get all successful scene video paths
        video_segments = []
        for frame in ctx.frames:
            if frame.video_segment_path and frame.status == "completed":
                video_segments.append(frame.video_segment_path)
        
        if not video_segments:
            raise RuntimeError("No successful scenes to concatenate")
        
        # Concatenate videos
        output_path = os.path.join(ctx.task_dir, "final_no_audio.mp4")
        await self.video.concat_videos(
            videos=video_segments,
            output=output_path,
            method="filter",
        )
        
        # Add BGM if configured
        bgm_path = ctx.config.bgm_path if hasattr(ctx.config, "bgm_path") and ctx.config.bgm_path else None
        bgm_volume = ctx.config.bgm_volume if hasattr(ctx.config, "bgm_volume") else 0.3
        
        if bgm_path:
            self._report_progress(
                ctx.progress_callback, "adding_bgm", 0.90,
                extra_info="正在添加背景音乐..."
            )
            
            output_with_bg_path = os.path.join(ctx.task_dir, "final_with_bg.mp4")
            await self.video.add_bgm(
                video=output_path,
                bgm=bgm_path,
                output=output_with_bg_path,
                bgm_volume=bgm_volume,
            )
            output_path = output_with_bg_path
        
        ctx.final_video_path = output_path
    
    async def finalize(self, ctx: PipelineContext) -> VideoGenerationResult:
        """Finalize and return result"""
        self._report_progress(
            ctx.progress_callback, "completed", 1.0,
            extra_info="动画视频生成完成！"
        )
        
        # Calculate total duration
        total_duration = sum(f.duration for f in ctx.frames if f.duration > 0)
        
        # Calculate file size
        file_size = 0
        if ctx.final_video_path and os.path.exists(ctx.final_video_path):
            file_size = os.path.getsize(ctx.final_video_path)
        
        # Update storyboard
        ctx.storyboard.final_video_path = ctx.final_video_path
        ctx.storyboard.total_duration = total_duration
        ctx.storyboard.completed_at = datetime.now()
        
        # Save metadata
        if self.core.persistence:
            await self.core.persistence.save_task_metadata(
                task_id=ctx.task_id,
                metadata={
                    "title": ctx.title,
                    "input_text": ctx.input_text,
                    "final_video_path": ctx.final_video_path,
                    "duration": total_duration,
                    "n_scenes": len(ctx.frames),
                    "animation_style": ctx.params.get("animation_style"),
                    "video_model": ctx.params.get("video_model"),
                },
            )
            
            # Save storyboard
            await self.core.persistence.save_storyboard(
                task_id=ctx.task_id,
                storyboard=ctx.storyboard,
            )
        
        # Create result
        result = VideoGenerationResult(
            video_path=ctx.final_video_path or "",
            storyboard=ctx.storyboard,
            duration=total_duration,
            file_size=file_size,
        )
        
        logger.info(f"Animation video completed: {ctx.title}, {total_duration:.1f}s, {file_size} bytes")
        
        return result
