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
Animation video prompt templates for script generation and style definitions
"""

# Animation script generation prompt template
ANIMATION_SCRIPT_PROMPT = """You are a professional animation director and screenwriter. Please create an animation script based on the following information:

Topic: {topic}
Animation Style: {style}
Characters: {characters}
Target Duration: {duration} seconds
Number of Scenes: {n_scenes}

Requirements:
1. Create {n_scenes} scenes with clear narrative structure (beginning, development, climax, conclusion)
2. Each scene should have:
   - Scene description (background, time, weather)
   - Characters present with their positions and initial expressions
   - Clear action descriptions
   - Dialogues (if any) with emotion tags
   - Camera setup (shot type and movement)
   - Special effects (if any)
3. Dialogues should be natural and fit character personalities
4. Include camera language (close-ups for emotions, wide shots for scenes)
5. Specify special effects timing and duration
6. Each scene should be 5-10 seconds

Output format: JSON with the following structure:
{{
  "title": "Video title",
  "style": "{style}",
  "total_duration": {duration},
  "characters": [
    {{
      "name": "Character name",
      "description": "Appearance description",
      "appearance": {{"gender": "male/female", "age_range": "young_adult", "hair": "...", "eyes": "...", "face": "...", "body": "..."}},
      "clothing": {{"outfit": "...", "accessories": "...", "colors": ["..."]}},
      "tts_voice": "zh-CN-YunxiNeural",
      "available_expressions": ["neutral", "smile", "angry", "surprised", "sad"],
      "available_actions": ["idle", "talking", "walking", "fighting", "casting_spell"]
    }}
  ],
  "scenes": [
    {{
      "index": 0,
      "description": "Scene description",
      "background": "Background description",
      "time_of_day": "day/night/sunset",
      "weather": "clear/rain/snow",
      "characters": [
        {{"character": "Character name", "position": "center/left/right", "initial_expression": "neutral", "initial_pose": "idle", "actions": []}}
      ],
      "action_description": "Action description",
      "dialogues": [
        {{"character": "Name", "text": "Dialogue text", "emotion": "smile/angry/etc", "start_time": 0.0, "end_time": 2.0}}
      ],
      "camera": {{"shot_type": "medium_shot", "movement": "static/zoom_in/pan_left", "movement_params": {{"speed": "medium"}}, "focus": "character", "focus_pull": false}},
      "effects": [
        {{"effect_type": "magic/weather/particle", "effect_name": "fireball/rain/speed_lines", "start_time": 0.0, "duration": 2.0, "intensity": 1.0, "color": "#FF0000", "description": "..."}}
      ],
      "duration": 5.0,
      "video_generation": {{"model": "ltx2.3", "resolution": "720x1280", "fps": 24, "guidance_scale": 7.0, "num_inference_steps": 50}}
    }}
  ],
  "global_settings": {{"bgm": "bgm/default.mp3", "bgm_volume": 0.3}}
}}

Please output ONLY the JSON, no additional text.
"""

# Animation style prompts
ANIMATION_STYLE_PROMPTS = {
    "fanren_xianxia": {
        "name": "凡人修仙传风格",
        "name_en": "FanRen Xianxia Style",
        "style_prefix": "Realistic 3D Chinese xianxia animation style, motion capture quality, UE5 Nanite detailed modeling, rich cinematic lighting, realistic character proportions, detailed facial expressions, flowing robes and hair, magical particle effects, cinematic composition, high quality animation, professional studio quality, 3D rendered",
        "color_grading": "cinematic_warm",
        "recommended_model": "ltx2.3"
    },
    "douluo_dalu": {
        "name": "斗罗大陆风格",
        "name_en": "Douluo Dalu Style",
        "style_prefix": "3D Chinese fantasy animation, soul ring effects, academy setting, dynamic combat, vibrant colors, detailed character design, magical martial souls, cinematic lighting, professional animation quality",
        "color_grading": "vibrant",
        "recommended_model": "ltx2.3"
    },
    "demon_slayer": {
        "name": "鬼灭之刃风格",
        "name_en": "Demon Slayer Style",
        "style_prefix": "Japanese anime style, ukiyo-e aesthetics, high contrast colors, dramatic lighting, volumetric light rays, traditional Japanese elements, detailed character design, expressive eyes with highlights, dynamic composition, fluid motion, 2D hand-drawn texture, professional anime production quality, studio ufotable style",
        "color_grading": "dramatic",
        "recommended_model": "wan2.2"
    },
    "jujutsu_kaisen": {
        "name": "咒术回战风格",
        "name_en": "Jujutsu Kaisen Style",
        "style_prefix": "Modern urban fantasy anime, domain expansion effects, dark color palette, dynamic action, detailed character animation, cursed energy effects, professional MAPPA studio quality, cinematic composition",
        "color_grading": "dark",
        "recommended_model": "wan2.2"
    },
    "disney_3d": {
        "name": "迪士尼3D风格",
        "name_en": "Disney 3D Style",
        "style_prefix": "Disney 3D animation style, cute characters, bright colors, smooth motion, family-friendly, expressive facial animation, high quality rendering, Pixar-like animation quality",
        "color_grading": "bright",
        "recommended_model": "ltx2.3"
    },
    "watercolor": {
        "name": "水墨风格",
        "name_en": "Watercolor Style",
        "style_prefix": "Chinese ink wash painting animation style, sumi-e, brush strokes, elegant linework, watercolor wash, poetic atmosphere, classical Chinese art, traditional animation",
        "color_grading": "soft",
        "recommended_model": "ltx2.3"
    },
    "cyberpunk": {
        "name": "赛博朋克风格",
        "name_en": "Cyberpunk Style",
        "style_prefix": "Cyberpunk anime style, neon lights, dark atmosphere, futuristic cityscape, high-tech low-life aesthetic, blue and pink color scheme, detailed mechanical elements, cinematic composition",
        "color_grading": "neon",
        "recommended_model": "ltx2.3"
    },
    "children": {
        "name": "儿童动画风格",
        "name_en": "Children Animation Style",
        "style_prefix": "Children's animation style, cute characters, bright colors, simple shapes, playful composition, child-friendly aesthetic, smooth motion, educational content style",
        "color_grading": "bright",
        "recommended_model": "ltx2.3"
    }
}

# Scene video generation prompt builder
def build_scene_video_prompt(style: str, scene, characters: list) -> str:
    """Build video generation prompt for a scene"""
    style_config = ANIMATION_STYLE_PROMPTS.get(style, {})
    style_prefix = style_config.get("style_prefix", "")
    
    # Character descriptions
    char_descriptions = []
    for char_in_scene in scene.get("characters", []):
        char_name = char_in_scene.get("character", "")
        # Find character config
        char_config = next((c for c in characters if c.get("name") == char_name), {})
        if char_config:
            desc = f"{char_config.get('appearance', {}).get('gender', '')} {char_config.get('appearance', {}).get('age_range', '')}, "
            desc += f"{char_config.get('appearance', {}).get('hair', '')}, "
            desc += f"{char_config.get('appearance', {}).get('face', '')}, "
            desc += f"wearing {char_config.get('clothing', {}).get('outfit', '')}"
            char_descriptions.append(desc)
    
    # Scene description
    scene_desc = f"{scene.get('background', '')}, {scene.get('time_of_day', '')}, {scene.get('weather', '')}"
    
    # Action description
    action_desc = scene.get("action_description", "")
    
    # Camera description
    camera = scene.get("camera", {})
    camera_desc = f"{camera.get('shot_type', 'medium_shot')}, {camera.get('movement', 'static')}"
    
    # Effects description
    effects = scene.get("effects", [])
    effects_desc = ", ".join([fx.get("description", "") for fx in effects if fx.get("description")])
    
    # Combine
    full_prompt = f"{style_prefix}, "
    if char_descriptions:
        full_prompt += f"{', '.join(char_descriptions)}, "
    full_prompt += f"{scene_desc}, "
    full_prompt += f"{action_desc}, "
    full_prompt += f"{camera_desc}, "
    if effects_desc:
        full_prompt += f"{effects_desc}, "
    full_prompt += "high quality, detailed, masterpiece, professional animation quality"
    
    return full_prompt
