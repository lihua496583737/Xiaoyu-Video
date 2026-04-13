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
Animation video data models for high-quality animation video generation
Supports character consistency, lip-sync, cinematic camera, and special effects
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class CharacterAppearanceConfig:
    """Character appearance configuration"""
    gender: str = "male"  # male/female/other
    age_range: str = "young_adult"  # child/teen/young_adult/adult/elderly
    hair: str = ""  # Hair style description
    eyes: str = ""  # Eye description
    face: str = ""  # Face description
    body: str = ""  # Body description
    height: str = ""  # Height description


@dataclass
class CharacterClothingConfig:
    """Character clothing configuration"""
    outfit: str = ""  # Main outfit description
    accessories: str = ""  # Accessories description
    colors: List[str] = field(default_factory=list)  # Primary colors


@dataclass
class CharacterConfig:
    """Character configuration for animation video"""
    name: str  # Character name
    description: str  # Overall appearance description
    
    # Appearance details
    appearance: CharacterAppearanceConfig = field(default_factory=CharacterAppearanceConfig)
    clothing: CharacterClothingConfig = field(default_factory=CharacterClothingConfig)
    
    # Reference images for consistency
    reference_images: List[str] = field(default_factory=list)
    # Recommended: front view, side view, face close-up, expression set (3-5 images)
    
    # Voice configuration
    tts_voice: str = "zh-CN-YunxiNeural"  # TTS voice ID
    tts_speed: float = 1.0  # Speech speed multiplier
    
    # Consistency configuration
    consistency_method: str = "ipadapter_faceid"  # ipadapter_faceid | reference_image | lora
    ipadapter_weight: float = 0.7  # IP-Adapter weight (0.5-0.9)
    lora_path: Optional[str] = None  # Character LoRA path (if available)
    seed: Optional[int] = None  # Fixed seed for reproducibility
    
    # Animation capabilities
    available_expressions: List[str] = field(default_factory=lambda: [
        "neutral", "smile", "laugh", "angry", "surprised", 
        "sad", "determined", "pained"
    ])
    available_actions: List[str] = field(default_factory=lambda: [
        "idle", "talking", "walking", "running", "fighting",
        "casting_spell", "drawing_sword", "waving", "pointing",
        "nodding", "shaking_head"
    ])
    
    # Metadata
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CharacterAction:
    """Character action in a scene"""
    action_type: str  # expression | movement | combat | spell
    action_name: str  # smile | walk_forward | cast_fireball | etc.
    start_time: float  # Start time relative to scene (seconds)
    duration: float  # Duration (seconds)
    intensity: float = 1.0  # Action intensity (0-1)


@dataclass
class CharacterInScene:
    """Character in a specific scene"""
    character: CharacterConfig
    position: str = "center"  # center/left/right/foreground/background
    initial_expression: str = "neutral"  # Initial expression
    initial_pose: str = "idle"  # Initial pose
    actions: List[CharacterAction] = field(default_factory=list)


@dataclass
class Dialogue:
    """Dialogue in a scene"""
    character: str  # Character name
    text: str  # Dialogue text
    emotion: str  # Emotion (triggers corresponding expression)
    start_time: float  # Start time relative to scene (seconds)
    end_time: float  # End time relative to scene (seconds)
    action_during_dialogue: Optional[str] = None  # Optional action during dialogue


@dataclass
class CameraSetup:
    """Camera setup for a scene"""
    shot_type: str = "medium_shot"  # close_up | medium_shot | wide_shot | extreme_wide | over_shoulder | pov
    movement: str = "static"  # static | zoom_in | zoom_out | pan_left | pan_right | tilt_up | tilt_down | follow | orbit | crane
    
    # Movement parameters
    movement_params: Dict[str, Any] = field(default_factory=lambda: {
        "speed": "medium",  # slow | medium | fast
        "start_zoom": 1.0,
        "end_zoom": 1.2,
    })
    
    # Focus
    focus: str = "character"  # Focus target
    focus_pull: bool = False  # Whether focus changes


@dataclass
class Effect:
    """Special effect in a scene"""
    effect_type: str  # magic | weather | particle | combat | environment
    effect_name: str  # fireball | lightning | rain | snow | speed_lines | explosion | aura
    start_time: float  # Start time relative to scene (seconds)
    duration: float  # Duration (seconds)
    intensity: float = 1.0  # Effect intensity (0-1)
    color: Optional[str] = None  # Effect color (hex)
    description: str = ""  # Effect description


@dataclass
class VideoGenerationConfig:
    """Video generation configuration for a scene"""
    model: str = "ltx2.3"  # ltx2.3 | wan2.2 | kling2.6 | vidu_q2
    
    # Generation parameters
    resolution: str = "720x1280"  # 720x1280 (9:16) | 1280x720 (16:9)
    fps: int = 24  # 24 | 30 | 48
    guidance_scale: float = 7.0  # Guidance scale
    num_inference_steps: int = 50  # Inference steps
    
    # Consistency parameters
    consistency_method: str = "ipadapter_faceid"
    reference_images: List[str] = field(default_factory=list)
    consistency_weight: float = 0.7
    
    # Post-processing
    upscale: bool = True  # Enable upscaling
    upscale_target: str = "1080x1920"  # Upscale target resolution
    interpolate: bool = True  # Enable frame interpolation
    interpolate_target_fps: int = 48  # Interpolation target FPS
    color_grade: bool = True  # Enable color grading


@dataclass
class SceneConfig:
    """Scene configuration for animation video"""
    index: int  # Scene index (0-based)
    description: str  # Scene description
    background: str  # Background description
    action_description: str  # "Han Li casts a spell, blue energy lightning surrounds"
    
    time_of_day: str = "day"  # day/night/sunset/dawn
    weather: str = "clear"  # clear/rain/snow/fog/storm
    
    # Background reference image (optional)
    background_image: Optional[str] = None
    
    # Characters in scene
    characters: List[CharacterInScene] = field(default_factory=list)
    
    # Dialogues
    dialogues: List[Dialogue] = field(default_factory=list)
    
    # Camera setup
    camera: CameraSetup = field(default_factory=CameraSetup)
    
    # Effects
    effects: List[Effect] = field(default_factory=list)
    
    # Duration
    duration: float = 5.0  # Scene duration (seconds)
    
    # Video generation config
    video_generation: VideoGenerationConfig = field(default_factory=VideoGenerationConfig)
    
    # Metadata
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class AnimationScript:
    """Complete animation video script"""
    title: str  # Video title
    style: str  # Animation style (e.g., "fanren_xianxia", "demon_slayer")
    total_duration: float  # Total duration (seconds)
    
    # Character list
    characters: List[CharacterConfig] = field(default_factory=list)
    
    # Scene list
    scenes: List[SceneConfig] = field(default_factory=list)
    
    # Global settings
    global_settings: Dict[str, Any] = field(default_factory=lambda: {
        "bgm": "bgm/default.mp3",
        "bgm_volume": 0.3,
        "subtitle_style": "anime",
        "color_grading": "cinematic",
    })
    
    # Metadata
    created_at: Optional[datetime] = None
    version: str = "1.0"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def n_scenes(self) -> int:
        """Number of scenes"""
        return len(self.scenes)
    
    @property
    def n_characters(self) -> int:
        """Number of characters"""
        return len(self.characters)


@dataclass
class SceneResult:
    """Result of processing a single scene"""
    scene_index: int
    video_path: str  # Processed scene video path
    duration: float  # Scene duration (seconds)
    quality_score: float  # Quality score (0-1)
    retry_count: int = 0  # Number of retries
    lip_sync_path: Optional[str] = None  # Lip-synced video path (if enabled)
    upscaled_path: Optional[str] = None  # Upscaled video path (if enabled)
    interpolated_path: Optional[str] = None  # Interpolated video path (if enabled)
    color_graded_path: Optional[str] = None  # Color graded video path (if enabled)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AnimationGenerationResult:
    """Animation video generation result"""
    video_path: str  # Final video path
    animation_script: AnimationScript  # Complete animation script
    scene_results: List[SceneResult]  # Results for each scene
    duration: float  # Total duration (seconds)
    file_size: int  # File size (bytes)
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def success_scenes(self) -> List[SceneResult]:
        """Get successfully processed scenes"""
        return [s for s in self.scene_results if s.video_path]
    
    @property
    def failed_scenes(self) -> List[SceneResult]:
        """Get failed scenes"""
        return [s for s in self.scene_results if not s.video_path]
    
    @property
    def average_quality(self) -> float:
        """Average quality score"""
        if not self.success_scenes:
            return 0.0
        return sum(s.quality_score for s in self.success_scenes) / len(self.success_scenes)
