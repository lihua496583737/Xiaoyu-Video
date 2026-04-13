# AI 高质量动画视频生成 - 全新设计方案

> **目标**：生成类似《凡人修仙传》《鬼灭之刃》质量的高清动画视频  
> **技术路线**：LTX 2.3 / Wan2.2 / Kling 2.6 + ComfyUI 生态 + RunningHub  
> **日期**：2026年4月8日  
> **状态**：全新设计（v2.0）

---

## 一、功能定义与核心价值

### 1.1 什么是 AI 高质量动画视频？

**目标效果**：生成质量接近专业动画工作室的短视频，类似：
- 🎬 **《凡人修仙传》** - 写实 3D 仙侠，动作捕捉质感，法术特效
- ⚔️ **《鬼灭之刃》** - 2D 手绘+3DCG 融合，浮世绘美学，呼吸法特效
- 🌟 **高质量 AI 动画短片** - 角色一致、动作流畅、特效精致

**核心特征**：
- ✅ **角色一致性** - 同一角色在不同镜头中外观高度一致
- ✅ **动作流畅** - 自然的角色动作、战斗、互动
- ✅ **口型同步** - 角色说话时口型与语音匹配
- ✅ **表情丰富** - 笑、哭、生气、惊讶等情感表达
- ✅ **特效精致** - 法术光效、粒子系统、天气效果
- ✅ **电影级运镜** - 推近、拉远、跟拍、环绕、俯冲
- ✅ **高清画质** - 1080p 起步，可达 4K

### 1.2 与现有视频的差异

| 维度 | 现有 StandardPipeline | 高质量动画视频 |
|------|----------------------|---------------|
| **画面类型** | 静态图像 + 字幕 | 动态动画（30-48fps） |
| **角色** | 无角色概念 | 可动画化角色，一致性高 |
| **动作** | 无 | 自然动作、战斗、互动 |
| **对话** | 底部字幕 | 口型同步 + 语音 |
| **特效** | 无 | 法术、粒子、天气、光影 |
| **镜头** | 无或简单 Ken Burns | 电影级运镜 |
| **生成技术** | AI 生图 + HTML 合成 | AI 视频生成 + ComfyUI 工作流 |
| **质量水平** | 中等 | 专业动画级别 |

### 1.3 应用场景

✅ **动画短片** - 原创动画 IP 创作  
✅ **仙侠/奇幻** - 小说改编动画、仙侠故事  
✅ **战斗场景** - 动作打斗、技能释放  
✅ **情感叙事** - 角色对话、情感互动  
✅ **产品宣传** - 动画风格的品牌宣传片  
✅ **教育培训** - 动画形式的教学内容  
✅ **社交媒体** - 抖音/B站/YouTube 动画短视频  

---

## 二、核心技术选型

### 2.1 视频生成模型对比

| 模型 | 角色一致性 | 时长 | 分辨率 | 质量 | 成本/10s | 适用场景 |
|------|-----------|------|--------|------|---------|---------|
| **LTX 2.3** ⭐ | ⭐⭐⭐⭐ | 6-10s | 720p→1080p | ⭐⭐⭐⭐ | 中 | **推荐**：细节清晰，支持 9:16 |
| **Wan2.2** ⭐ | ⭐⭐⭐⭐ | 5s | 480p/720p | ⭐⭐⭐⭐ | 中 | **推荐**：电影感强，MoE 架构 |
| **Wan2.6** | ⭐⭐⭐⭐⭐ | 15s | 720p | ⭐⭐⭐⭐⭐ | 高 | 精品：支持多镜头叙事、口型同步 |
| **Kling 2.6** ⭐ | ⭐⭐⭐⭐⭐ | 10s | 1080p | ⭐⭐⭐⭐⭐ | 中高 | **推荐**：角色一致性最强，中文理解好 |
| **Vidu Q2** | ⭐⭐⭐⭐⭐ | 8-32s | 未公开 | ⭐⭐⭐ | 低 | 批量：多角色锁定，性价比高 |
| **CogVideoX 1.5** | ⭐⭐⭐ | 5-10s | 768p | ⭐⭐⭐ | 低（本地） | 开源：适合本地部署 |
| **MiniMax Hailuo 2.3** | ⭐⭐⭐ | 6-10s | 1080p | ⭐⭐⭐⭐ | 中 | 相机控制好 |

### 2.2 推荐技术栈

```yaml
# MVP 技术栈（推荐）
mvp_tech_stack:
  # 视频生成（核心）
  video_generation:
    primary: "LTX 2.3"  # 主力模型
      reason: "开源、22B 参数、细节清晰、支持 9:16、角色一致性好"
    secondary: "Wan2.2"  # 备选
      reason: "电影感强、MoE 架构、ComfyUI 支持好"
    premium: "Kling 2.6"  # 高质量选项
      reason: "角色一致性最强、中文理解好、口型同步"
  
  # 角色一致性方案
  character_consistency:
    approach_1: "IP-Adapter FaceID Plus"  # 首选
      reason: "ComfyUI 主流方案，面部锁定效果好"
    approach_2: "首帧参考（Image-to-Video）"  # 简单方案
      reason: "所有视频模型原生支持"
    approach_3: "BindWeave（针对 Wan2.2）"  # Wan 专用
      reason: "Wan 视频角色一致性专用方案"
    approach_4: "角色 LoRA（长期方案）"  # 高质量
      reason: "为固定角色训练专用 LoRA"
  
  # 口型同步
  lip_sync:
    approach_1: "Wav2Lip"  # 开源方案
      reason: "成熟稳定，ComfyUI 有节点"
    approach_2: "SadTalker"  # 备选
      reason: "表情更自然"
    approach_3: "Kling 2.6 原生口型同步"  # 商业方案
      reason: "音画同出，质量最高"
  
  # 执行平台
  execution_platform:
    primary: "RunningHub"  # 云端执行
      reason: "无需本地 GPU、支持所有主流模型、API 成熟"
    secondary: "本地 ComfyUI"  # 本地执行
      reason: "成本低、可定制、需要高显存 GPU"
  
  # 辅助技术
  auxiliary:
    controlnet: "姿态/构图控制"
    upscaler: "视频超分（720p→1080p）"
    interpolation: "帧插值（24fps→48fps）"
    color_grading: "色彩校正/风格统一"
```

### 2.3 RunningHub 工作流准备

**需要准备的 ComfyUI 工作流**：

```
workflows/
├── runninghub/
│   ├── video_ltx2.3_anime.json          # LTX 2.3 动画生成
│   ├── video_ltx2.3_i2v.json            # LTX 2.3 图生视频
│   ├── video_wan2.2_anime.json          # Wan2.2 动画生成
│   ├── video_wan2.2_i2v.json            # Wan2.2 图生视频
│   ├── video_kling2.6_anime.json        # Kling 2.6 动画生成
│   ├── video_character_consistency.json # 角色一致性增强
│   ├── video_lip_sync.json              # 口型同步
│   ├── video_upscale.json               # 视频超分
│   ├── video_interpolation.json         # 帧插值
│   └── video_color_grading.json         # 色彩校正
└── selfhost/
    └── ... (同上，本地部署版)
```

---

## 三、核心数据模型设计

### 3.1 角色模型

```python
@dataclass
class CharacterConfig:
    """角色配置（用于动画生成）"""
    # 基本信息
    name: str  # 角色名
    description: str  # 外观描述（详细）
    
    # 角色外观
    appearance: dict = field(default_factory=lambda: {
        "gender": "male",  # male/female
        "age_range": "young_adult",  # child/teen/young_adult/adult/elderly
        "hair": "黑色长发，飘逸",  # 发型描述
        "eyes": "深邃的黑色眼睛",  # 眼睛描述
        "face": "英俊的面容，棱角分明",  # 面部描述
        "body": "修长健美的身材",  # 身材描述
        "height": "180cm",  # 身高
    })
    
    # 服饰
    clothing: dict = field(default_factory=lambda: {
        "outfit": "青色修仙长袍，绣有金色纹路",  # 服装
        "accessories": "腰间佩戴玉佩，手持长剑",  # 配饰
        "colors": ["青色", "金色", "白色"],  # 主要颜色
    })
    
    # 角色参考图（用于一致性）
    reference_images: List[str] = field(default_factory=list)
    # 建议提供：
    # - 正面全身图
    # - 侧面全身图
    # - 正面脸部特写
    # - 不同表情图（3-5 张）
    
    # 语音配置
    tts_voice: str = "zh-CN-YunxiNeural"  # TTS 音色
    tts_speed: float = 1.0  # 语速
    
    # 一致性配置
    consistency_method: str = "ipadapter_faceid"  # ipadapter_faceid | reference_image | lora
    ipadapter_weight: float = 0.7  # IP-Adapter 权重
    lora_path: Optional[str] = None  # 角色 LoRA 路径（如果有）
    seed: Optional[int] = None  # 固定种子
    
    # 动画能力
    available_expressions: List[str] = field(default_factory=lambda: [
        "neutral",  # 中性
        "smile",  # 微笑
        "laugh",  # 大笑
        "angry",  # 生气
        "surprised",  # 惊讶
        "sad",  # 悲伤
        "determined",  # 坚定
        "pained",  # 痛苦
    ])
    
    available_actions: List[str] = field(default_factory=lambda: [
        "idle",  # 待机
        "talking",  # 说话
        "walking",  # 走路
        "running",  # 跑步
        "fighting",  # 战斗
        "casting_spell",  # 施法
        "drawing_sword",  # 拔剑
        "waving",  # 挥手
        "pointing",  # 指物
        "nodding",  # 点头
        "shaking_head",  # 摇头
    ])
```

### 3.2 场景模型

```python
@dataclass
class SceneConfig:
    """场景配置"""
    index: int  # 场景索引
    
    # 场景描述
    description: str  # 场景描述
    background: str  # 背景描述
    time_of_day: str = "day"  # day/night/sunset/dawn
    weather: str = "clear"  # clear/rain/snow/fog/storm
    
    # 场景参考图（可选）
    background_image: Optional[str] = None
    
    # 出场角色
    characters: List[CharacterInScene] = field(default_factory=list)
    
    # 动作描述
    action_description: str  # "韩立施展青色法术，蓝色光效环绕"
    
    # 对话
    dialogues: List[Dialogue] = field(default_factory=list)
    
    # 镜头设置
    camera: CameraSetup = field(default_factory=CameraSetup)
    
    # 特效
    effects: List[Effect] = field(default_factory=list)
    
    # 时长
    duration: float = 5.0  # 秒（建议 5-10 秒）
    
    # 视频生成设置
    video_generation: VideoGenerationConfig = field(default_factory=VideoGenerationConfig)

@dataclass
class CharacterInScene:
    """场景中的角色"""
    character: CharacterConfig
    position: str = "center"  # center/left/right/foreground/background
    initial_expression: str = "neutral"  # 初始表情
    initial_pose: str = "idle"  # 初始姿势
    actions: List[CharacterAction] = field(default_factory=list)  # 动作列表

@dataclass
class CharacterAction:
    """角色动作"""
    action_type: str  # "expression" | "movement" | "combat" | "spell"
    action_name: str  # "smile" | "walk_forward" | "cast_fireball" | etc.
    start_time: float  # 相对场景开始的时间（秒）
    duration: float  # 持续时间（秒）
    intensity: float = 1.0  # 动作强度（0-1）

@dataclass
class Dialogue:
    """对话"""
    character: str  # 角色名
    text: str  # 对话内容
    emotion: str  # 情感（触发对应表情）
    start_time: float  # 对话开始时间
    end_time: float  # 对话结束时间
    action_during_dialogue: Optional[str] = None  # 对话中的动作

@dataclass
class CameraSetup:
    """镜头设置"""
    # 镜头类型
    shot_type: str = "medium_shot"  # close_up | medium_shot | wide_shot | extreme_wide | over_shoulder | pov
    
    # 镜头运动
    movement: str = "static"  # static | zoom_in | zoom_out | pan_left | pan_right | tilt_up | tilt_down | follow | orbit | crane
    
    # 运动参数
    movement_params: dict = field(default_factory=lambda: {
        "speed": "medium",  # slow | medium | fast
        "start_zoom": 1.0,
        "end_zoom": 1.2,
    })
    
    # 焦点
    focus: str = "character"  # 焦点目标
    focus_pull: bool = False  # 是否有焦点变化

@dataclass
class Effect:
    """特效"""
    effect_type: str  # "magic" | "weather" | "particle" | "combat" | "environment"
    effect_name: str  # "fireball" | "lightning" | "rain" | "snow" | "speed_lines" | "explosion" | "aura"
    start_time: float
    duration: float
    intensity: float = 1.0
    color: Optional[str] = None  # 特效颜色
    description: str = ""  # 特效描述

@dataclass
class VideoGenerationConfig:
    """视频生成配置"""
    # 使用的模型
    model: str = "ltx2.3"  # ltx2.3 | wan2.2 | kling2.6 | vidu_q2
    
    # 生成参数
    resolution: str = "720x1280"  # 720x1280 (9:16) | 1280x720 (16:9)
    fps: int = 24  # 24 | 30 | 48
    guidance_scale: float = 7.0  # 引导系数
    num_inference_steps: int = 50  # 推理步数
    
    # 一致性参数
    consistency_method: str = "ipadapter_faceid"
    reference_images: List[str] = field(default_factory=list)
    consistency_weight: float = 0.7
    
    # 后期处理
    upscale: bool = True  # 是否超分
    upscale_target: str = "1080x1920"  # 超分目标分辨率
    interpolate: bool = True  # 是否帧插值
    interpolate_target_fps: int = 48  # 插值目标帧率
    color_grade: bool = True  # 是否色彩校正
```

### 3.3 动画脚本模型

```python
@dataclass
class AnimationScript:
    """动画脚本"""
    title: str  # 标题
    style: str  # 动画风格（如 "凡人修仙传风格"）
    total_duration: float  # 总时长（秒）
    
    # 角色列表
    characters: List[CharacterConfig] = field(default_factory=list)
    
    # 场景列表
    scenes: List[SceneConfig] = field(default_factory=list)
    
    # 全局设置
    global_settings: dict = field(default_factory=lambda: {
        "bgm": "bgm/default.mp3",
        "bgm_volume": 0.3,
        "subtitle_style": "anime",
        "color_grading": "cinematic",
    })
    
    # 元数据
    created_at: Optional[datetime] = None
    version: str = "1.0"
```

---

## 四、核心业务流程设计

### 4.1 完整动画生成流程

```
┌──────────────────────────────────────────────────────────────┐
│                  AI 高质量动画视频生成流程                      │
│                                                              │
│  输入: 主题/故事 + 角色定义 + 风格选择                          │
│  输出: 高质量动画视频（1080p, 30-48fps）                       │
│                                                              │
│  预计时间: 30-90 分钟（取决于场景数量和复杂度）                  │
│  预计成本: 10-50 元（RunningHub）                              │
└──────────────────────────────────────────────────────────────┘

Step 1: 生成动画脚本
  ├─ 输入: 主题、角色、风格、时长
  ├─ 处理: LLM 生成动画脚本（含场景、对话、动作、特效、运镜）
  ├─ 输出: AnimationScript JSON
  ├─ 耗时: 10-30 秒
  └─ 成本: 0.01-0.05 元

Step 2: 准备角色参考图
  ├─ 输入: 角色描述
  ├─ 处理: AI 生成角色参考图（正面、侧面、表情集）
  ├─ 输出: 角色参考图集（3-5 张/角色）
  ├─ 耗时: 30-60 秒/角色
  └─ 成本: 0.1-0.3 元/角色

Step 3: 生成场景背景（可选）
  ├─ 输入: 场景描述
  ├─ 处理: AI 生成背景图
  ├─ 输出: 背景图集
  ├─ 耗时: 20-40 秒/场景
  └─ 成本: 0.05-0.15 元/场景

Step 4: 逐场景生成动画视频 ⭐ 核心步骤
  ├─ 对每个场景:
  │   ├─ 4.1 加载角色参考图和场景设置
  │   ├─ 4.2 构建视频生成提示词
  │   │   └─ [风格] + [角色] + [场景] + [动作] + [特效] + [镜头]
  │   ├─ 4.3 调用视频生成模型（LTX 2.3 / Wan2.2 / Kling 2.6）
  │   │   ├─ 使用 IP-Adapter FaceID 保持角色一致性
  │   │   ├─ 使用 ControlNet 控制姿态/构图
  │   │   └─ 应用风格化 LoRA（可选）
  │   ├─ 4.4 质量检查
  │   │   ├─ 角色一致性检查
  │   │   ├─ 动作流畅度检查
  │   │   └─ 提示词匹配度检查
  │   ├─ 4.5 如果不合格，重试（最多 3 次）
  │   └─ 4.6 输出场景视频片段（5-10 秒，720p/1080p）
  ├─ 输出: 场景视频片段列表
  ├─ 耗时: 2-5 分钟/场景（含重试）
  └─ 成本: 1-5 元/场景

Step 5: 口型同步处理（如果有对话）
  ├─ 输入: 场景视频 + TTS 音频
  ├─ 处理: Wav2Lip / SadTalker 生成口型同步
  ├─ 输出: 口型同步视频
  ├─ 耗时: 30-60 秒/场景
  └─ 成本: 0.1-0.3 元/场景

Step 6: 视频后期处理
  ├─ 6.1 视频超分（720p → 1080p）
  │   ├─ 耗时: 1-2 分钟/场景
  │   └─ 成本: 0.2-0.5 元/场景
  ├─ 6.2 帧插值（24fps → 48fps，可选）
  │   ├─ 耗时: 1-2 分钟/场景
  │   └─ 成本: 0.2-0.5 元/场景
  ├─ 6.3 色彩校正/风格统一
  │   ├─ 耗时: 30-60 秒/场景
  │   └─ 成本: 0.1-0.2 元/场景
  └─ 输出: 后处理视频片段

Step 7: 场景拼接与转场
  ├─ 输入: 后处理视频片段
  ├─ 处理: 
  │   ├─ 按顺序拼接场景
  │   ├─ 应用场景间转场（淡入淡出、溶解、划像等）
  │   └─ 确保视频连续性
  ├─ 输出: 完整视频（无音频）
  ├─ 耗时: 30-60 秒
  └─ 成本: 0.05 元

Step 8: 音频合成
  ├─ 8.1 生成 TTS 音频（所有对话）
  │   ├─ 耗时: 10-30 秒
  │   └─ 成本: 0.01 元
  ├─ 8.2 添加音效（按时间线）
  │   ├─ 法术音效、战斗音效、环境音效
  │   └─ 耗时: 10-30 秒
  ├─ 8.3 添加 BGM
  │   ├─ 循环适配视频时长
  │   └─ 音量平衡
  └─ 输出: 完整音频轨

Step 9: 最终合成
  ├─ 输入: 视频 + 音频
  ├─ 处理:
  │   ├─ 合并视频和音频
  │   ├─ 添加字幕（可选）
  │   ├─ 添加片头片尾（可选）
  │   └─ 最终质量检查
  ├─ 输出: 最终动画视频（MP4, 1080p, 48fps）
  ├─ 耗时: 30-60 秒
  └─ 成本: 0.05 元

Step 10: 持久化元数据
  ├─ 保存 AnimationScript JSON
  ├─ 保存所有中间文件
  ├─ 更新索引
  └─ 返回结果
```

### 4.2 提示词工程

**视频生成提示词模板**：

```python
# 凡人修仙传风格
FANREN_STYLE_PROMPT = """
Realistic 3D Chinese xianxia animation style, motion capture quality, 
UE5 Nanite detailed modeling, rich cinematic lighting, 
realistic character proportions, detailed facial expressions, 
flowing robes and hair, magical particle effects, 
cinematic composition, high quality animation, 
professional studio quality, 3D rendered
"""

# 鬼灭之刃风格
DEMON_SLAYER_STYLE_PROMPT = """
Japanese anime style, ukiyo-e aesthetics, high contrast colors, 
dramatic lighting, volumetric light rays, traditional Japanese elements, 
detailed character design, expressive eyes with highlights, 
dynamic composition, fluid motion, 2D hand-drawn texture, 
professional anime production quality, studio ufotable style
"""

# 完整提示词构建
def build_video_generation_prompt(
    style: str,
    scene: SceneConfig,
    characters: List[CharacterConfig]
) -> str:
    """构建视频生成提示词"""
    
    # 风格前缀
    style_prefix = STYLE_PROMPTS.get(style, "")
    
    # 角色描述
    char_descriptions = []
    for char_in_scene in scene.characters:
        char = char_in_scene.character
        desc = f"{char.appearance['gender']} {char.appearance['age_range']}, "
        desc += f"{char.appearance['hair']}, "
        desc += f"{char.appearance['face']}, "
        desc += f"wearing {char.clothing['outfit']}, "
        desc += f"with {char.clothing['accessories']}"
        char_descriptions.append(desc)
    
    # 场景描述
    scene_desc = f"{scene.background}, {scene.time_of_day}, {scene.weather}"
    
    # 动作描述
    action_desc = scene.action_description
    
    # 镜头描述
    camera_desc = f"{scene.camera.shot_type}, {scene.camera.movement}"
    
    # 特效描述
    effects_desc = ", ".join([fx.description for fx in scene.effects])
    
    # 组合
    full_prompt = f"{style_prefix}, "
    full_prompt += f"{', '.join(char_descriptions)}, "
    full_prompt += f"{scene_desc}, "
    full_prompt += f"{action_desc}, "
    full_prompt += f"{camera_desc}, "
    if effects_desc:
        full_prompt += f"{effects_desc}, "
    full_prompt += f"high quality, detailed, masterpiece"
    
    return full_prompt

# 示例
example_prompt = build_video_generation_prompt(
    style="fanren_xianxia",
    scene=SceneConfig(
        description="山巅对决",
        background="云雾缭绕的山巅，古老的松树",
        time_of_day="sunset",
        weather="clear",
        action_description="韩立双手结印，青色法术光球在手中凝聚，蓝色能量闪电环绕",
        camera=CameraSetup(shot_type="medium_shot", movement="zoom_in"),
        effects=[Effect(effect_type="magic", effect_name="qi_ball", description="青色法术光球，蓝色闪电环绕")]
    ),
    characters=[...角色列表...]
)

# 输出提示词：
# "Realistic 3D Chinese xianxia animation style, motion capture quality, 
#  UE5 Nanite detailed modeling, rich cinematic lighting, ...
#  male young_adult, 黑色长发，飘逸, 英俊的面容，棱角分明, 
#  wearing 青色修仙长袍，绣有金色纹路, with 腰间佩戴玉佩，手持长剑, 
#  云雾缭绕的山巅，古老的松树, sunset, clear, 
#  韩立双手结印，青色法术光球在手中凝聚，蓝色能量闪电环绕, 
#  medium_shot, zoom_in, 
#  青色法术光球，蓝色闪电环绕, 
#  high quality, detailed, masterpiece"
```

### 4.3 角色一致性保障方案

```yaml
# 多层次角色一致性保障
character_consistency_strategy:
  # 层级 1: 提示词工程
  level_1_prompt:
    - "详细的角色外观描述"
    - "固定角色关键词"
    - "风格锁定词"
    - "质量提升词"
  
  # 层级 2: 参考图（IP-Adapter FaceID）
  level_2_ipadapter:
    - "上传角色正面脸部参考图"
    - "IP-Adapter FaceID Plus 节点"
    - "权重 0.6-0.8"
    - "面部特征锁定"
  
  # 层级 3: 首帧控制（Image-to-Video）
  level_3_first_frame:
    - "使用角色参考图作为首帧"
    - "图生视频模式（I2V）"
    - "保持初始外观"
  
  # 层级 4: ControlNet 姿态控制
  level_4_controlnet:
    - "使用 OpenPose 控制姿态"
    - "确保动作符合预期"
    - "避免奇怪姿势"
  
  # 层级 5: 种子固定
  level_5_seed:
    - "同一角色使用相同种子"
    - "提高可重复性"
  
  # 层级 6: 角色 LoRA（长期方案）
  level_6_lora:
    - "为重要角色训练专用 LoRA"
    - "需要 15-30 张角色图"
    - "训练成本：5-20 元/角色"
    - "效果最佳"
```

---

## 五、Web UI 设计

### 5.1 用户界面流程

```
┌──────────────────────────────────────────────────────────────┐
│              AI 动画视频生成 - Web UI 流程                     │
└──────────────────────────────────────────────────────────────┘

Step 1: 选择动画风格
  ├─ [🎨] 凡人修仙传风格（3D 写实仙侠）
  ├─ [⚔️] 鬼灭之刃风格（2D 手绘战斗）
  ├─ [🌟] 原创动画风格
  ├─ [🎭] 自定义风格
  └─ [📚] 查看更多风格（27+ 种）

Step 2: 定义角色
  ├─ [➕] 添加角色按钮
  ├─ 对每个角色:
  │   ├─ 名称: [输入框]
  │   ├─ 外观描述: [文本域]
  │   ├─ 服饰描述: [文本域]
  │   ├─ 上传参考图: [文件上传]（可选，3-5 张推荐）
  │   │   └─ 预览网格（3 列）
  │   ├─ TTS 音色: [下拉选择]
  │   └─ 一致性方法: [单选]
  │       ├─ IP-Adapter（推荐）
  │       ├─ 参考图（简单）
  │       └─ LoRA（高质量，需训练）
  └─ 角色预览卡片

Step 3: 输入故事/脚本
  ├─ 方式 A: 简单模式
  │   ├─ 输入主题: [文本域]
  │   ├─ 目标时长: [滑块]（10-120 秒）
  │   ├─ 场景数量: [滑块]（3-8 个）
  │   └─ [✨] 自动生成脚本按钮
  │
  ├─ 方式 B: 高级模式
  │   ├─ 手动编辑动画脚本 JSON
  │   ├─ 可视化脚本编辑器
  │   └─ 逐场景配置
  │
  └─ 方式 C: 上传脚本
      ├─ 上传 JSON 文件
      └─ 自动解析

Step 4: 配置生成设置
  ├─ 视频模型: [下拉选择]
  │   ├─ LTX 2.3（推荐）
  │   ├─ Wan2.2（电影感）
  │   └─ Kling 2.6（最高质量）
  ├─ 分辨率: [下拉选择]
  │   ├─ 720x1280（竖屏 9:16）
  │   └─ 1280x720（横屏 16:9）
  ├─ 帧率: [下拉选择]（24/30/48）
  ├─ 后期处理: [复选框]
  │   ├─ ☑ 视频超分（720p→1080p）
  │   ├─ ☑ 帧插值（24fps→48fps）
  │   └─ ☑ 色彩校正
  ├─ 角色一致性强度: [滑块]（0.5-1.0）
  └─ 最大重试次数: [数字输入]（1-3）

Step 5: 配置音频
  ├─ TTS 设置:
  │   ├─ 语速: [滑块]（0.5x-2.0x）
  │   └─ 音色: [每个角色独立选择]
  ├─ 音效: [复选框]
  │   ├─ ☑ 法术音效
  │   ├─ ☑ 战斗音效
  │   ├─ ☑ 环境音效
  │   └─ ☑ 转场音效
  └─ BGM:
      ├─ 选择 BGM: [下拉选择]
      └─ BGM 音量: [滑块]

Step 6: 预览和生成
  ├─ [📋] 脚本预览（可编辑）
  ├─ [💰] 成本估算（显示详细分解）
  ├─ [⏱️] 时间估算
  ├─ [🚀] 生成动画视频按钮
  └─ 进度条（详细分阶段显示）

Step 7: 查看结果
  ├─ 视频播放器
  ├─ [⬇️] 下载按钮
  ├─ [🔄] 重新生成（可调整参数）
  ├─ [✏️] 编辑并重新生成特定场景
  └─ [📊] 生成报告（成本、耗时、质量评分）
```

### 5.2 成本估算显示

```yaml
# 成本估算示例（5 个场景，LTX 2.3）
cost_estimate:
  breakdown:
    llm_script_generation: 0.03 元
    character_reference_images: 0.5 元 (2 角色 × 0.25 元)
    background_images: 0.3 元 (3 场景 × 0.1 元)
    video_generation: 15.0 元 (5 场景 × 3.0 元，含重试)
    lip_sync: 1.0 元 (5 场景 × 0.2 元)
    upscaling: 2.5 元 (5 场景 × 0.5 元)
    interpolation: 2.5 元 (5 场景 × 0.5 元)
    color_grading: 1.0 元 (5 场景 × 0.2 元)
    audio_synthesis: 0.1 元
    final_composite: 0.05 元
  
  total: 23.0 元
  range: "18-28 元" (考虑重试和变化)
  
  # 优化建议
  optimization_tips:
    - "关闭帧插值可节省 2.5 元（质量影响：中等）"
    - "减少场景数量到 3 个可节省约 6 元"
    - "使用 Wan2.2 代替 LTX 2.3 可节省约 30% 成本"
    - "使用本地 ComfyUI 可节省 80% 视频生成成本"
```

---

## 六、技术实现要点

### 6.1 ComfyUI 工作流设计

**LTX 2.3 动画生成工作流**：

```json
{
  "workflow_name": "video_ltx2.3_anime",
  "description": "LTX 2.3 高质量动画视频生成",
  "source": "runninghub",
  "workflow_id": "待分配",
  
  "nodes": {
    "1_prompt_input": {
      "class_type": "PrimitiveStringMultiline",
      "_meta": {"title": "$prompt"},
      "inputs": {"value": ""}
    },
    
    "2_negative_prompt": {
      "class_type": "PrimitiveStringMultiline",
      "_meta": {"title": "negative_prompt"},
      "inputs": {"value": "low quality, blurry, deformed, ugly, bad anatomy, disfigured, poorly drawn face, mutation, extra limb, watermark, text"}
    },
    
    "3_ipadapter_loader": {
      "class_type": "IPAdapterModelLoader",
      "inputs": {
        "ipadapter_file": "ip-adapter-faceid-plus_sd15.safetensors"
      }
    },
    
    "4_ipadapter_apply": {
      "class_type": "IPAdapterApplyFaceID",
      "inputs": {
        "ipadapter": ["3_ipadapter_loader", 0],
        "image": ["$reference_image", 0],
        "weight": "$consistency_weight"
      }
    },
    
    "5_controlnet_loader": {
      "class_type": "ControlNetLoader",
      "inputs": {
        "control_net_name": "control_v11p_sd15_openpose.safetensors"
      }
    },
    
    "6_ltx2.3_model": {
      "class_type": "LTX2VideoModelLoader",
      "inputs": {
        "model_path": "ltx-video-2.3.safetensors"
      }
    },
    
    "7_ltx2.3_vae": {
      "class_type": "LTX2VAELoader",
      "inputs": {
        "vae_path": "ltx-video-2.3-vae.safetensors"
      }
    },
    
    "8_ltx2.3_generate": {
      "class_type": "LTX2VideoGeneration",
      "inputs": {
        "model": ["6_ltx2.3_model", 0],
        "vae": ["7_ltx2.3_vae", 0],
        "prompt": ["1_prompt_input", 0],
        "negative_prompt": ["2_negative_prompt", 0],
        "ipadapter_condition": ["4_ipadapter_apply", 0],
        "controlnet": ["5_controlnet_loader", 0],
        "controlnet_image": ["$pose_image", 0],
        "width": 720,
        "height": 1280,
        "num_frames": 144,
        "fps": 24,
        "guidance_scale": "$guidance_scale",
        "num_inference_steps": "$num_steps",
        "seed": "$seed"
      }
    },
    
    "9_vae_decode": {
      "class_type": "VAEDecode",
      "inputs": {
        "samples": ["8_ltx2.3_generate", 0],
        "vae": ["7_ltx2.3_vae", 0]
      }
    },
    
    "10_upscale": {
      "class_type": "VideoUpscaleModel",
      "inputs": {
        "images": ["9_vae_decode", 0],
        "upscale_model": "realesrgan-x4plus.pth",
        "target_resolution": [1080, 1920]
      }
    },
    
    "11_interpolation": {
      "class_type": "FrameInterpolation",
      "inputs": {
        "images": ["10_upscale", 0],
        "target_fps": 48,
        "method": "rife"
      }
    },
    
    "12_save_video": {
      "class_type": "VHS_VideoCombine",
      "inputs": {
        "images": ["11_interpolation", 0],
        "frame_rate": 48,
        "filename_prefix": "animation_scene",
        "format": "video/h264-mp4",
        "crf": 19
      }
    }
  },
  
  "parameter_mapping": {
    "$prompt": "text",
    "$reference_image": "image_path",
    "$pose_image": "image_path (optional)",
    "$consistency_weight": "float (0.5-0.9)",
    "$guidance_scale": "float (5.0-9.0)",
    "$num_steps": "int (30-75)",
    "$seed": "int (optional)"
  }
}
```

### 6.2 错误处理和重试

```python
class AnimationVideoPipeline(LinearVideoPipeline):
    """高质量动画视频生成 Pipeline"""
    
    async def produce_assets(self, ctx: PipelineContext):
        """生成资产（带完善的错误处理）"""
        
        for i, scene in enumerate(ctx.animation_script.scenes):
            max_attempts = ctx.params.get("max_retries", 3)
            last_error = None
            
            for attempt in range(max_attempts):
                try:
                    # 1. 构建提示词
                    prompt = self._build_scene_prompt(
                        scene, 
                        ctx.animation_script.characters,
                        ctx.animation_script.style
                    )
                    
                    # 2. 准备参考图
                    reference_images = self._prepare_reference_images(
                        scene.characters
                    )
                    
                    # 3. 调用视频生成
                    logger.info(f"Scene {i+1}/{len(ctx.animation_script.scenes)}, Attempt {attempt+1}")
                    video_path = await self._generate_scene_video(
                        prompt=prompt,
                        reference_images=reference_images,
                        config=scene.video_generation
                    )
                    
                    # 4. 质量检查
                    quality_score = await self._check_video_quality(
                        video_path,
                        expected_characters=scene.characters,
                        prompt=prompt
                    )
                    
                    if quality_score >= 0.7:
                        logger.info(f"Scene {i+1} passed quality check (score: {quality_score})")
                        scene.video_path = video_path
                        scene.quality_score = quality_score
                        break
                    else:
                        logger.warning(f"Scene {i+1} quality score {quality_score} < 0.7, retrying...")
                        last_error = f"Quality check failed: {quality_score}"
                        # 调整参数重试
                        self._adjust_generation_params(scene, attempt)
                
                except VideoGenerationError as e:
                    logger.error(f"Scene {i+1} generation error: {e}")
                    last_error = str(e)
                    
                    if attempt < max_attempts - 1:
                        # 等待后重试
                        await asyncio.sleep(5 * (attempt + 1))
                    continue
                
                except Exception as e:
                    logger.exception(f"Scene {i+1} unexpected error: {e}")
                    last_error = str(e)
                    break
            
            # 检查是否成功
            if scene.video_path is None:
                logger.error(f"Scene {i+1} failed after {max_attempts} attempts")
                scene.status = "failed"
                scene.error = last_error
                
                # 决定是否继续或中止
                if ctx.params.get("fail_fast", False):
                    raise RuntimeError(f"Scene {i+1} failed: {last_error}")
                else:
                    logger.warning(f"Continuing with failed scene {i+1}")
            
            # 报告进度
            progress = (i + 1) / len(ctx.animation_script.scenes)
            self._report_progress(
                ctx.progress_callback,
                "scene_completed",
                progress,
                frame_current=i + 1,
                frame_total=len(ctx.animation_script.scenes),
                extra_info=f"Scene {i+1}/{len(ctx.animation_script.scenes)} completed"
            )
        
        # 检查是否有足够的成功场景
        success_scenes = [s for s in ctx.animation_script.scenes if s.video_path]
        if len(success_scenes) < len(ctx.animation_script.scenes) * 0.6:
            raise RuntimeError(
                f"Too many scenes failed: {len(success_scenes)}/{len(ctx.animation_script.scenes)}"
            )
```

### 6.3 进度反馈设计

```python
# 详细的进度事件
class AnimationProgressEvent:
    EVENTS = {
        # 脚本生成
        "generating_script": {"base_progress": 0.02, "message": "正在生成动画脚本..."},
        "script_completed": {"base_progress": 0.05, "message": "动画脚本生成完成"},
        
        # 角色准备
        "generating_character_refs": {
            "base_progress": 0.05,
            "weight": 0.10,
            "message_template": "正在生成角色参考图 ({current}/{total}): {char_name}"
        },
        
        # 背景生成
        "generating_backgrounds": {
            "base_progress": 0.15,
            "weight": 0.05,
            "message_template": "正在生成背景 ({current}/{total})"
        },
        
        # 场景视频生成（核心）
        "generating_scene_video": {
            "base_progress": 0.20,
            "weight": 0.50,  # 占 50% 时间
            "message_template": "正在生成场景 {current}/{total} 视频 (尝试 {attempt}/3)..."
        },
        "scene_video_retry": {
            "message_template": "场景 {scene_index} 质量不佳，重试中..."
        },
        "scene_video_completed": {
            "message_template": "场景 {scene_index} 视频生成完成 (质量评分: {quality_score})"
        },
        
        # 口型同步
        "applying_lip_sync": {
            "base_progress": 0.70,
            "weight": 0.05,
            "message_template": "正在应用口型同步 ({current}/{total})"
        },
        
        # 后期处理
        "upscaling_video": {
            "base_progress": 0.75,
            "weight": 0.10,
            "message_template": "正在超分视频 ({current}/{total})"
        },
        "interpolating_frames": {
            "base_progress": 0.85,
            "weight": 0.05,
            "message_template": "正在帧插值 ({current}/{total})"
        },
        "color_grading": {
            "base_progress": 0.90,
            "weight": 0.03,
            "message_template": "正在色彩校正"
        },
        
        # 合成
        "compiling_scenes": {"base_progress": 0.93, "message": "正在拼接场景..."},
        "adding_audio": {"base_progress": 0.96, "message": "正在合成音频..."},
        "final_composite": {"base_progress": 0.98, "message": "正在最终合成..."},
        
        # 完成
        "completed": {
            "base_progress": 1.0,
            "message": "动画视频生成完成！"
        }
    }
```

---

## 七、风格库设计

### 7.1 预设风格（27 种）

```yaml
animation_styles:
  # 中国 3D 仙侠系列 (5种)
  - id: fanren_xianxia
    name: "凡人修仙传风格"
    category: chinese_3d_xianxia
    description: "写实 3D 仙侠，动作捕捉质感，法术特效"
    style_prompt: "Realistic 3D Chinese xianxia animation, motion capture quality, UE5 Nanite modeling, rich cinematic lighting, flowing robes, magical particle effects"
    recommended_model: "ltx2.3"
    aspect_ratio: "9:16"
    color_grading: "cinematic_warm"
    
  - id: douluo_dalu
    name: "斗罗大陆风格"
    category: chinese_3d_xianxia
    description: "3D 奇幻战斗，魂环特效，学院风格"
    style_prompt: "3D Chinese fantasy animation, soul ring effects, academy setting, dynamic combat, vibrant colors"
    
  - id: xian_ni
    name: "仙逆风格"
    category: chinese_3d_xianxia
    description: "暗黑仙侠，冷峻色调，强大气场"
    style_prompt: "Dark Chinese xianxia 3D animation, cold color tone, powerful aura, intense atmosphere"
    
  # 日本 2D 动画系列 (6种)
  - id: demon_slayer
    name: "鬼灭之刃风格"
    category: japanese_2d_anime
    description: "浮世绘美学，呼吸法特效，高对比度色彩"
    style_prompt: "Japanese anime style, ukiyo-e aesthetics, high contrast colors, dramatic lighting, volumetric light, breathing technique effects"
    recommended_model: "wan2.2"
    
  - id: jujutsu_kaisen
    name: "咒术回战风格"
    category: japanese_2d_anime
    description: "现代都市奇幻，领域展开，暗色调"
    style_prompt: "Modern urban fantasy anime, domain expansion effects, dark color palette, dynamic action"
    
  - id: attack_on_titan
    name: "进击的巨人风格"
    category: japanese_2d_anime
    description: "史诗战斗，宏大场景，紧张氛围"
    style_prompt: "Epic battle anime, grand scale scenes, intense atmosphere, dramatic composition"
  
  # 通用动画系列 (8种)
  - id: disney_3d
    name: "迪士尼 3D 风格"
    category: western_3d_animation
    description: "迪士尼式 3D 动画，可爱角色，明亮色彩"
    style_prompt: "Disney 3D animation style, cute characters, bright colors, smooth motion, family-friendly"
  
  # ... 更多风格

  # 总计：27 种风格
```

### 7.2 用户自定义风格

```yaml
# 支持用户上传自定义风格
custom_styles:
  # 方式 1: 提示词定义
  prompt_based:
    name: "我的自定义风格"
    custom_prompt: "赛博朋克风格，霓虹灯光，未来都市..."
    negative_prompt: "low quality, blurry..."
  
  # 方式 2: 参考图定义
  reference_based:
    name: "基于参考图的风格"
    reference_images:
      - "path/to/style_ref_1.png"
      - "path/to/style_ref_2.png"
    style_transfer_strength: 0.7
  
  # 方式 3: LoRA 定义
  lora_based:
    name: "基于 LoRA 的风格"
    lora_path: "data/loras/my_custom_style.safetensors"
    lora_weight: 0.8
```

---

## 八、成本和性能优化

### 8.1 成本优化策略

```yaml
cost_optimization:
  # 策略 1: 模型选择
  model_selection:
    budget_tier_1:  # 低成本（5-10 元）
      - model: "wan2.2"
      - skip_upscaling: true
      - skip_interpolation: true
      - max_scenes: 3
    
    budget_tier_2:  # 中成本（10-30 元）
      - model: "ltx2.3"
      - enable_upscaling: true
      - skip_interpolation: true
      - max_scenes: 5
    
    budget_tier_3:  # 高成本（30-100 元）
      - model: "kling2.6"
      - enable_upscaling: true
      - enable_interpolation: true
      - enable_color_grading: true
      - max_scenes: 8
  
  # 策略 2: 本地 vs 云端
  execution_location:
    runninghub:
      pros: ["无需本地 GPU", "支持所有模型", "API 成熟"]
      cons: ["成本较高", "依赖网络"]
      cost_multiplier: 1.0
    
    local_comfyui:
      pros: ["成本低", "可定制", "无网络依赖"]
      cons: ["需要高显存 GPU", "设置复杂"]
      cost_multiplier: 0.2  # 约为 RunningHub 的 20%
  
  # 策略 3: 批量生成
  batch_generation:
    - "多个场景批量生成，享受折扣"
    - "共享角色参考图，减少重复生成"
    - "复用相同背景，减少生成次数"
```

### 8.2 性能优化策略

```yaml
performance_optimization:
  # 策略 1: 并发控制
  concurrency:
    max_concurrent_scenes: 3  # 最大并发生成场景数
    semaphore: "asyncio.Semaphore(3)"
  
  # 策略 2: 缓存
  caching:
    character_reference_images: "缓存角色参考图"
    background_images: "缓存常用背景"
    style_prompts: "缓存风格提示词"
  
  # 策略 3: 分层生成
  layered_generation:
    - "先生成低分辨率预览"
    - "用户确认后再生成高分辨率"
    - "避免不满意场景的高成本生成"
  
  # 策略 4: 智能重试
  smart_retry:
    - "质量检查失败时分析原因"
    - "根据原因调整提示词或参数"
    - "避免无效重试"
```

---

## 九、关键风险和解决方案

### 9.1 技术风险

| 风险 | 影响 | 概率 | 解决方案 |
|------|------|------|---------|
| **角色一致性不佳** | 🔴 高 | 🟡 中 | IP-Adapter + 首帧控制 + LoRA（多层保障） |
| **视频生成失败** | 🔴 高 | 🟡 中 | 重试机制 + 质量检查 + 降级方案 |
| **生成时间过长** | 🟡 中 | 🔴 高 | 并发控制 + 缓存 + 分层生成 |
| **成本超出预期** | 🟡 中 | 🟡 中 | 成本估算 + 预算控制 + 优化建议 |
| **口型同步不自然** | 🟡 中 | 🟡 中 | Wav2Lip + SadTalker 对比 + 手动调整 |
| **特效质量不佳** | 🟡 中 | 🟡 中 | 预设特效库 + 后期合成 |
| **ComfyUI 工作流不兼容** | 🔴 高 | 🟢 低 | 提前测试 + 版本锁定 |

### 9.2 质量风险

| 风险 | 解决方案 |
|------|---------|
| **动作不自然** | ControlNet 姿态控制 + 预设动作库 |
| **表情僵硬** | Wav2Lip 口型同步 + 表情插值 |
| **特效穿模** | 后期 AE 合成 + 手动调整 |
| **镜头抖动** | 稳定器滤镜 + 平滑处理 |
| **色彩不统一** | 色彩校正 + 风格统一 LoRA |

---

## 十、开发计划

### 10.1 阶段规划

| 阶段 | 时间 | 目标 | 交付物 |
|------|------|------|--------|
| **MVP** | 4 周 | 基础动画生成（LTX 2.3 + IP-Adapter） | 可生成 3-5 场景动画，角色一致性基础保障 |
| **阶段 2** | 4 周 | 口型同步 + 后期处理 | 完整口型同步、超分、帧插值 |
| **阶段 3** | 4 周 | 多模型支持 + 风格扩展 | 支持 Wan2.2/Kling 2.6、27 种风格 |
| **阶段 4** | 4 周 | 高级功能 + 优化 | 角色 LoRA 训练、批量生成、性能优化 |

### 10.2 MVP 功能清单

- ✅ 选择动画风格（5 种基础风格）
- ✅ 定义角色（外观描述 + 参考图上传）
- ✅ LLM 生成动画脚本
- ✅ 生成角色参考图
- ✅ 逐场景生成视频（LTX 2.3）
- ✅ IP-Adapter 角色一致性
- ✅ 基础质量检查
- ✅ 视频拼接 + 转场
- ✅ TTS 配音
- ✅ Web UI（简单模式）
- ✅ 进度反馈
- ✅ 错误处理和重试

---

## 十一、总结

### 11.1 核心价值

✅ **高质量动画** - 接近专业动画工作室质量  
✅ **角色一致性** - 多层保障（IP-Adapter + 首帧控制 + LoRA）  
✅ **口型同步** - 自然的对话动画  
✅ **电影级运镜** - 专业的镜头语言  
✅ **丰富特效** - 法术、粒子、天气、战斗  
✅ **灵活扩展** - 27+ 种风格，支持自定义  
✅ **成本控制** - 分层生成，预算可控  

### 11.2 技术可行性

基于当前 AI 视频生成技术（LTX 2.3、Wan2.2、Kling 2.6）和 ComfyUI 生态，生成高质量动画视频**完全可行**，但需要注意：

⚠️ **角色一致性** - 需要多层保障，不能仅靠提示词  
⚠️ **生成时间** - 单视频 30-90 分钟，需要用户耐心  
⚠️ **成本** - 10-50 元/视频，需要成本控制  
⚠️ **质量波动** - AI 生成有随机性，需要质量检查和重试  

### 11.3 与现有管道的统一改进

通过分析现有管道（数字人、图生视频、动作迁移），本设计吸取了教训：

✅ **完善的错误处理** - 多层 try-except + 重试机制  
✅ **详细的进度反馈** - 12+ 个进度节点  
✅ **功能分层** - 简单/高级/自定义模式  
✅ **参数可选** - 所有参数有默认值  
✅ **成本估算** - 生成前显示详细成本  
✅ **质量检查** - 自动生成后质量评估  

---

**文档状态**：全新设计完成 ✅  
**下一步**：评审 → 确定方案 → 开始实现

*创建时间：2026年4月8日*  
*版本：v2.0*
