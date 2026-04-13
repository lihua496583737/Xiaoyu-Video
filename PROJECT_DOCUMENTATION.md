# XiaoYu.AI 项目详细说明文档

> **AI 全自动短视频引擎** - 输入主题即可自动生成包含文案、AI 配图/视频、语音解说和背景音乐的完整视频

---

## 目录

- [一、项目概述](#一项目概述)
- [二、技术选型](#二技术选型)
- [三、项目架构](#三项目架构)
- [四、核心业务模块](#四核心业务模块)
- [五、模块关系图](#五模块关系图)
- [六、业务流程详解](#六业务流程详解)
- [七、API 接口文档](#七-api-接口文档)
- [八、前端架构](#八前端架构)
- [九、配置说明](#九配置说明)
- [十、部署方式](#十部署方式)

---

## 一、项目概述

### 1.1 项目简介

**XiaoYu.AI** 是一个基于 AI 的全自动短视频生成平台，采用模块化设计，用户只需输入一个主题，系统即可自动完成从内容创作、图像/视频生成、语音合成到最终视频合成的完整流程。

**核心能力**：
- 输入主题 → 自动生成完整短视频
- 支持 AI 全自动生成（文案+画面+配音+背景音乐）
- 支持用户上传自有素材生成视频
- 支持数字人口播、图生视频、动作迁移等多种模式
- 提供 Web UI 和 REST API 两种使用方式

**项目信息**：
- 项目名称：`XiaoYu.AI`
- 版本：`0.1.15`
- 许可证：Apache 2.0
- Python 版本：>= 3.11

### 1.2 应用场景

- 自媒体短视频内容批量生产
- 营销推广视频制作
- 知识科普类视频生成
- 情感/心理/养生类图文视频
- 数字人直播带货视频
- 产品宣传视频

---

## 二、技术选型

### 2.1 后端技术栈

| 技术 | 用途 | 说明 |
|------|------|------|
| **FastAPI** | Web 框架 | 高性能异步 Python Web 框架，自动生成交互式 API 文档 |
| **Uvicorn** | ASGI 服务器 | 支持异步 IO 的高性能 ASGI 服务器 |
| **Pydantic** | 数据验证 | 基于类型提示的数据验证和序列化库 |
| **OpenAI SDK** | LLM 集成 | 兼容所有 OpenAI 接口的 LLM 服务（Qwen/GPT-4o/DeepSeek/Claude/Ollama 等） |
| **ComfyKit** | ComfyUI 引擎 | 用于执行 ComfyUI 工作流，支持 RunningHub 云服务和自部署 |
| **FFmpeg + ffmpeg-python** | 视频处理 | 视频拼接、音频合并、图像叠加等核心视频处理 |
| **Edge TTS** | 语音合成 | 微软免费开源的 TTS 引擎，支持多语言语音 |
| **html2image + Chromium** | HTML 渲染 | 将 HTML 模板渲染为图像，支持字幕叠加 |
| **asyncio** | 异步处理 | Python 原生异步支持，用于并发任务处理 |

### 2.2 前端技术栈

| 技术 | 用途 | 说明 |
|------|------|------|
| **Streamlit** | Web UI 框架 | 纯 Python 构建的交互式 Web 应用 |
| **loguru** | 日志 | Python 日志库 |
| **httpx** | HTTP 客户端 | 异步 HTTP 请求 |

### 2.3 AI 模型和工作流

| 类别 | 模型/工作流 | 用途 |
|------|------------|------|
| **大语言模型** | Qwen / GPT-4o / DeepSeek / Claude / Ollama | 文案生成、提示词生成、标题生成内容创作 |
| **图像生成** | Flux / SDXL / Qwen 文生图 | AI 配图/海报/卡片生成 |
| **视频生成** | Wan2.1 / Wan2.2 / LTX2 | AI 视频片段生成 |
| **图像分析** | Florence-2 / BLIP | 分析用户上传的图片内容 |
| **视频分析** | Qwen3-VL | 分析用户上传的视频内容 |
| **语音合成** | Edge TTS / Index-TTS | 文字转语音，支持声音克隆 |

### 2.4 存储方案

| 类型 | 方案 | 说明 |
|------|------|------|
| **任务元数据** | JSON 文件系统 | 基于文件系统的持久化，存储在 `output/` 目录 |
| **索引** | `.index.json` | 任务索引文件，加速列表查询 |
| **媒体文件** | 本地文件系统 | 音频/图像/视频文件存储在 `output/{task_id}/frames/` 目录 |
| **任务状态** | 内存（可扩展 Redis） | 当前使用内存字典，支持替换为 Redis |

---

## 三、项目架构

### 3.1 整体架构分层

```
┌─────────────────────────────────────────────────────────────────┐
│                          用户界面层                               │
│  ┌─────────────────┐         ┌──────────────────────┐            │
│  │   Streamlit Web │         │   REST API 客户端     │            │
│  │   (Python UI)   │         │   (Postman/cURL/SDK)  │            │
│  └────────┬────────┘         └──────────┬───────────┘            │
└───────────┼─────────────────────────────┼────────────────────────┘
            │                             │
┌───────────┼─────────────────────────────┼────────────────────────┐
│           ↓         FastAPI 后端层      ↓                        │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                  FastAPI 应用入口                         │    │
│  │  - CORS 中间件                                           │    │
│  │  - 路由注册                                               │    │
│  │  - 依赖注入 (PixelleVideoCore)                            │    │
│  └────────────────────────┬─────────────────────────────────┘    │
│                           │                                      │
│  ┌────────────────────────┴──────────────────────────────────┐    │
│  │                    API 路由层                              │    │
│  │  ┌─────┐ ┌────┐ ┌─────┐ ┌──────┐ ┌─────┐ ┌──────┐        │    │
│  │  │LLM  │ │TTS │ │Image│ │Video │ │Tasks│ │Files │ ...    │    │
│  │  └─────┘ └────┘ └─────┘ └──────┘ └─────┘ └──────┘        │    │
│  └────────────────────────┬──────────────────────────────────┘    │
│                           │                                      │
│  ┌────────────────────────┴──────────────────────────────────┐    │
│  │                    任务管理层                              │    │
│  │  ┌──────────────┐        ┌───────────────┐                │    │
│  │  │  TaskManager  │        │  Task Models  │                │    │
│  │  │  (异步执行)   │        │  (生命周期)   │                │    │
│  │  └──────────────┘        └───────────────┘                │    │
│  └────────────────────────┬──────────────────────────────────┘    │
└───────────────────────────┼──────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                           ↓   核心业务层                          │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │              PixelleVideoCore (核心服务入口)                 │   │
│  │  ┌─────┐ ┌─────┐ ┌──────┐ ┌──────┐ ┌──────────┐           │   │
│  │  │ LLM │ │ TTS │ │Media │ │Video │ │FrameProc │           │   │
│  │  └─────┘ └─────┘ └──────┘ └──────┘ └──────────┘           │   │
│  │  ┌──────────────┐  ┌───────────────┐  ┌──────────┐         │   │
│  │  │Persistence   │  │HistoryManager │  │ComfyKit  │         │   │
│  │  └──────────────┘  └───────────────┘  └──────────┘         │   │
│  └────────────────────────┬───────────────────────────────────┘   │
│                           │                                        │
│  ┌────────────────────────┴───────────────────────────────────┐   │
│  │                    流水线层                                 │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌───────────────┐       │   │
│  │  │ Standard     │ │ AssetBased   │ │  Custom       │       │   │
│  │  │ Pipeline     │ │ Pipeline     │ │  Pipeline     │       │   │
│  │  └──────────────┘ └──────────────┘ └───────────────┘       │   │
│  └────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                           ↓   AI 服务层                          │
│  ┌──────────────────┐   ┌──────────────────┐                     │
│  │   ComfyUI 工作流  │   │   OpenAI 兼容 API │                    │
│  │  - RunningHub    │   │  - Qwen          │                     │
│  │  - Self-hosted   │   │  - GPT-4o        │                     │
│  └──────────────────┘   │  - DeepSeek      │                     │
│                          │  - Claude        │                     │
│                          │  - Ollama        │                     │
│                          └──────────────────┘                     │
└────────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                           ↓   基础设施层                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐      │
│  │  FFmpeg  │  │ Chromium │  │ Edge TTS │  │ 文件系统    │      │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────┘      │
└────────────────────────────────────────────────────────────────────┘
```

### 3.2 目录结构

```
Xiaoyu-Video/
├── api/                              # FastAPI 后端服务
│   ├── app.py                        # 应用入口
│   ├── config.py                     # API 配置
│   ├── dependencies.py               # 依赖注入
│   ├── routers/                      # API 路由 (10个模块)
│   │   ├── content.py                # 内容生成
│   │   ├── files.py                  # 文件管理
│   │   ├── frame.py                  # 帧处理
│   │   ├── health.py                 # 健康检查
│   │   ├── image.py                  # 图片生成
│   │   ├── llm.py                    # LLM 调用
│   │   ├── resources.py              # 资源管理
│   │   ├── tasks.py                  # 任务管理
│   │   ├── tts.py                    # TTS 合成
│   │   └── video.py                  # 视频生成
│   ├── schemas/                      # Pydantic 数据模型
│   └── tasks/                        # 异步任务管理
│
├── pixelle_video/                    # 核心业务逻辑模块
│   ├── service.py                    # 核心服务类 (PixelleVideoCore)
│   ├── config/                       # 配置管理
│   │   ├── schema.py                 # Pydantic 配置模型
│   │   ├── manager.py                # 配置管理器 (单例)
│   │   └── loader.py                 # YAML 加载器
│   ├── models/                       # 数据模型
│   │   ├── storyboard.py             # 故事板和分镜模型
│   │   ├── progress.py               # 进度事件模型
│   │   └── media.py                  # 媒体结果模型
│   ├── pipelines/                    # 视频生成流水线
│   │   ├── base.py                   # 流水线基类
│   │   ├── linear.py                 # 线性流水线 (模板方法模式)
│   │   ├── standard.py               # 标准 AI 生成流水线
│   │   ├── asset_based.py            # 素材驱动流水线
│   │   └── custom.py                 # 自定义流水线
│   ├── services/                     # 核心服务实现
│   │   ├── llm_service.py            # LLM 服务
│   │   ├── tts_service.py            # TTS 服务
│   │   ├── media.py                  # 媒体生成服务
│   │   ├── video.py                  # 视频处理服务
│   │   ├── frame_processor.py        # 帧处理器
│   │   ├── frame_html.py             # HTML 帧渲染
│   │   ├── comfy_base_service.py     # ComfyUI 基础服务
│   │   ├── persistence.py            # 持久化服务
│   │   ├── history_manager.py        # 历史管理器
│   │   ├── image_analysis.py         # 图像分析服务
│   │   └── video_analysis.py         # 视频分析服务
│   ├── prompts/                      # AI 提示词模板
│   │   ├── content_narration.py      # 内容旁白提示词
│   │   ├── topic_narration.py        # 主题旁白提示词
│   │   ├── image_generation.py       # 图像生成提示词
│   │   ├── video_generation.py       # 视频生成提示词
│   │   ├── title_generation.py       # 标题生成提示词
│   │   └── ...
│   └── utils/                        # 工具函数
│       ├── content_generators.py     # 内容生成工具
│       ├── llm_util.py               # LLM 工具
│       ├── tts_util.py               # TTS 工具
│       ├── template_util.py          # 模板工具
│       └── workflow_util.py          # 工作流工具
│
├── web/                              # Streamlit Web 前端
│   ├── app.py                        # 主入口
│   ├── pages/                        # 页面
│   │   ├── 1_🎬_Home.py              # 首页 (视频生成)
│   │   └── 2_📚_History.py           # 历史记录页
│   ├── components/                   # UI 组件
│   │   ├── content_input.py          # 内容输入
│   │   ├── style_config.py           # 样式配置
│   │   ├── output_preview.py         # 输出预览
│   │   ├── settings.py               # 系统设置
│   │   └── ...
│   ├── pipelines/                    # Web 端流水线 (插件式)
│   │   ├── base.py                   # PipelineUI 基类
│   │   ├── standard.py               # 快速创作管道
│   │   ├── asset_based.py            # 素材驱动管道
│   │   ├── digital_human.py          # 数字人口播管道
│   │   ├── i2v.py                    # 图生视频管道
│   │   └── action_transfer.py        # 动作迁移管道
│   ├── state/                        # 状态管理
│   └── i18n/                         # 国际化
│
├── workflows/                        # ComfyUI 工作流配置
│   ├── runninghub/                   # 云端工作流 (21个)
│   └── selfhost/                     # 本地工作流 (8个)
│
├── templates/                        # 视频 HTML 模板 (31个)
│   ├── 1080x1920/                    # 竖屏/肖像 (25个)
│   ├── 1080x1080/                    # 方形 (1个)
│   └── 1920x1080/                    # 横屏 (5个)
│
├── bgm/                              # 背景音乐
├── resources/                        # 静态资源
├── docs/                             # 文档 (MkDocs)
├── packaging/                        # 打包发布
├── pyproject.toml                    # 项目配置
├── docker-compose.yml                # Docker 编排
└── config.example.yaml               # 配置模板
```

---

## 四、核心业务模块

### 4.1 核心服务入口 (PixelleVideoCore)

**文件**：`pixelle_video/service.py`

`PixelleVideoCore` 是整个系统的中枢，统一封装所有 AI 能力：

```python
class PixelleVideoCore:
    # 服务组件
    self.llm           # LLMService - OpenAI SDK 兼容
    self.tts           # TTSService - Edge TTS + ComfyUI
    self.media         # MediaService - 图像/视频生成
    self.video         # VideoService - FFmpeg 处理
    self.frame_processor  # FrameProcessor - 帧处理编排
    self.persistence      # PersistenceService - JSON 文件持久化
    self.history          # HistoryManager - 历史记录
    
    # 流水线注册
    self.pipelines = {
        "standard": StandardPipeline(self),     # 默认 AI 生成
        "custom": CustomPipeline(self),         # 自定义模板
        "asset_based": AssetBasedPipeline(self), # 用户素材驱动
    }
```

**关键特性**：
- **ComfyKit 懒加载**：首次使用时创建，配置变更自动检测并重建实例
- **多流水线支持**：支持切换不同的视频生成流水线
- **热重载配置**：配置变更无需重启服务

### 4.2 LLM 服务模块

**文件**：`pixelle_video/services/llm_service.py`

**功能**：
- 集成 OpenAI AsyncOpenAI SDK，兼容所有 OpenAI 接口提供商
- 支持结构化输出（Pydantic 模型）
- JSON 解析容错（直接解析 → markdown 代码块提取 → 任意 JSON 提取）
- 动态配置读取，支持热重载

**使用场景**：
- 根据主题自动生成旁白文案
- 根据内容生成图像提示词（Image Prompt）
- 生成视频标题
- 分析用户素材并生成场景分配方案

**支持的 LLM 预设**：
- Qwen（通义千问）
- GPT-4o
- DeepSeek
- Kimi
- Ollama（本地部署）
- 自定义 OpenAI 兼容 API

### 4.3 TTS 语音合成模块

**文件**：`pixelle_video/services/tts_service.py`

**功能**：
- 支持双模式推理：
  - **本地模式**：Edge TTS（免费，无需 ComfyUI）
  - **ComfyUI 模式**：通过 ComfyKit 执行工作流（支持声音克隆）
- 支持语音克隆（ref_audio 参数）
- 自动处理音频 URL 下载到本地

**支持的 TTS 音色**：
- Edge TTS：多语言、多音色选择
- Index-TTS：支持声音克隆
- 星火 TTS：通过 ComfyUI 工作流

### 4.4 媒体生成模块

**文件**：`pixelle_video/services/media.py`

**功能**：
- 统一图像和视频生成服务
- 扫描 `image_*` 和 `video_*` 前缀的工作流
- 返回 `MediaResult` 对象（media_type + url + duration）
- 支持 TTS 音频时长驱动视频生成（音画同步）

**工作流类型**：
- 图像生成：Flux、SDXL、Qwen 文生图等
- 视频生成：Wan2.1、Wan2.2、LTX2 等

### 4.5 视频处理模块

**文件**：`pixelle_video/services/video.py`

**功能**：
- **视频拼接**：`concat_videos()` - 多个视频片段拼接（demuxer/filter 两种方法）
- **音视频合并**：`merge_audio_video()` - 智能合并（自动处理时长差异、填充/裁剪）
- **透明图像叠加**：`overlay_image_on_video()` - 支持 contain/cover/stretch 缩放
- **静态图像转视频**：`create_video_from_image()` - 图像+音频生成视频
- **背景音乐添加**：`add_bgm_to_video()` - 添加背景音乐
- **视频时长填充**：`_pad_video_to_duration()` - 最后帧冻结/黑屏填充
- **视频时长裁剪**：`_trim_video_to_duration()` - 裁剪到目标时长

**智能时长处理策略**：
```python
if video_duration < audio_duration:
    填充视频（最后帧冻结或黑屏）
elif video_duration > audio_duration + tolerance:
    裁剪视频到音频时长
else:
    保持原样（差异在容忍范围内）
```

### 4.6 帧处理模块 (FrameProcessor)

**文件**：`pixelle_video/services/frame_processor.py`

**功能**：帧处理编排器，处理单个 StoryboardFrame 的完整流程

**处理步骤**：
1. **生成音频**（TTS）- 使用旁白文本生成语音
2. **生成媒体**（图像/视频）- 使用 AI 工作流生成配图
3. **合成帧**（HTML 模板）- 使用 HTML 模板渲染帧图像（带字幕）
4. **创建视频片段** - 将媒体+音频+字幕合成为视频片段

**关键设计**：
- TTS 驱动的时长控制：音频时长传递给视频工作流，确保音画同步
- 智能跳过：如果模板不需要图像/视频，跳过生成步骤（静态模板更快/更便宜）
- 支持进度回调（ProgressEvent）

### 4.7 HTML 渲染模块

**文件**：`pixelle_video/services/frame_html.py`

**功能**：
- 使用 `html2image` 库 + Chromium 渲染 HTML 模板
- 支持变量替换语法 `{{param:type=default}}`
- 自动从模板路径解析尺寸
- 支持透明背景渲染（用于视频叠加）
- Chromium bug 修复：额外渲染 87px 后裁剪

**模板类型**：
- `static_*.html`：静态模板（无需 AI 生成媒体）
- `image_*.html`：需要 AI 生成图像
- `video_*.html`：需要 AI 生成视频

### 4.8 持久化服务模块

**文件**：`pixelle_video/services/persistence.py`

**功能**：
- 基于 JSON 文件的任务元数据和分镜脚本持久化
- 目录结构：`output/{task_id}/metadata.json`, `storyboard.json`, `frames/`
- 索引管理：`.index.json` 快速查询
- 支持分页查询（`list_tasks_paginated`）
- 统计信息（`get_statistics`）

**输出目录结构**：
```
output/
├── {task_id}/
│   ├── metadata.json          # 任务元数据
│   ├── storyboard.json        # 故事板数据
│   ├── final.mp4              # 最终视频
│   └── frames/
│       ├── 01_audio.mp3       # TTS 音频
│       ├── 01_image.png       # AI 生成的图像
│       ├── 01_composed.png    # HTML 合成的帧图像
│       ├── 01_segment.mp4     # 视频片段
│       └── ...
└── .index.json                # 快速索引文件
```

### 4.9 历史管理器

**文件**：`pixelle_video/services/history_manager.py`

**功能**：
- 查询历史任务列表
- 获取任务详情
- 删除任务
- 支持分页和筛选

### 4.10 图像/视频分析模块

**图像分析**：`pixelle_video/services/image_analysis.py`
- 使用 ComfyUI 工作流（Florence-2/BLIP）分析图像
- 生成图像的文字描述
- 用于资产驱动流水线

**视频分析**：`pixelle_video/services/video_analysis.py`
- 使用 ComfyUI 工作流（Qwen3-VL）分析视频内容
- 生成视频的文字描述
- 用于资产驱动流水线

---

## 五、模块关系图

### 5.1 模块依赖关系

```
┌──────────────────────────────────────────────────────────────┐
│                        用户请求                               │
│                  (Web UI / API 客户端)                        │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                     FastAPI 路由层                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │video.py  │ │tasks.py  │ │files.py  │ │resources.py│        │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘         │
│       │             │             │             │              │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐         │
│  │image.py  │ │llm.py    │ │tts.py    │ │frame.py  │         │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘         │
└───────┼─────────────┼─────────────┼─────────────┼─────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
                      ↓
┌──────────────────────────────────────────────────────────────┐
│                   PixelleVideoCore                           │
│                  (核心服务入口)                                │
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐            │
│  │    Pipelines        │  │    Services         │            │
│  │  ┌──────────────┐   │  │  ┌──────────────┐   │            │
│  │  │ Standard     │   │  │  │ LLMService   │   │            │
│  │  │ AssetBased   │───┼──┼──│ TTSService   │   │            │
│  │  │ Custom       │   │  │  │ MediaService │   │            │
│  │  └──────────────┘   │  │  │ VideoService │   │            │
│  └─────────────────────┘  │  │ FrameProcessor│   │            │
│                           │  │ Persistence  │   │            │
│                           │  └──────────────┘   │            │
│                           └─────────────────────┘            │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                      AI 服务层                                │
│  ┌──────────────────┐  ┌──────────────────┐                  │
│  │ ComfyUI/RunningHub│  │ OpenAI 兼容 API  │                  │
│  │ - 图像生成        │  │ - 文案生成        │                  │
│  │ - 视频生成        │  │ - 提示词生成      │                  │
│  │ - TTS            │  │ - 分析理解        │                  │
│  └──────────────────┘  └──────────────────┘                  │
└──────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                      基础设施层                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐      │
│  │  FFmpeg  │ │ Chromium │ │ Edge TTS │ │ 文件系统    │      │
│  └──────────┘ └──────────┘ └──────────┘ └─────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 数据流关系

```
用户输入 (主题/脚本/素材)
         │
         ├──→ LLM 服务 ──→ 生成旁白/标题/提示词
         │
         ├──→ TTS 服务 ──→ 生成音频 (决定时长)
         │                      │
         │                      ↓
         ├──→ Media 服务 ──→ 生成图像/视频 (根据音频时长)
         │                      │
         │                      ↓
         ├──→ HTML 渲染 ──→ 合成帧图像 (添加字幕)
         │                      │
         │                      ↓
         ├──→ Video 服务 ──→ 创建视频片段 (媒体+音频+字幕)
         │                      │
         │                      ↓ (逐帧重复)
         │
         ├──→ Video 服务 ──→ 拼接所有视频片段
         │                      │
         │                      ↓
         └──→ Video 服务 ──→ 添加背景音乐 ──→ 最终视频
                                    │
                                    ↓
                          Persistence 服务 ──→ 保存元数据
```

---

## 六、业务流程详解

### 6.1 标准 AI 自动生成流程 (StandardPipeline)

这是最核心的业务流程，用户只需输入一个主题，系统即可自动生成完整视频。

#### 流程概览

```
输入主题
  ↓
生成旁白文案
  ↓
生成视频标题
  ↓
生成图像提示词
  ↓
创建故事板
  ↓
逐帧处理 (TTS → 媒体生成 → HTML 合成 → 视频片段)
  ↓
拼接视频
  ↓
添加背景音乐
  ↓
输出最终视频
```

#### 详细步骤

**Step 1: 环境准备**
```
- 创建任务目录：output/{task_id}/
- 初始化配置和参数
```

**Step 2: 生成旁白文案**
- **generate 模式**：LLM 根据主题自动生成
  - 调用 `generate_narrations_from_topic()`
  - 使用提示词模板 `topic_narration.py`
  - 输出：旁白文本列表
- **fixed 模式**：使用用户提供的固定脚本
  - 调用 `split_narration_script()`
  - 支持 paragraph/line/sentence 分割模式
  - 输出：旁白文本列表

**Step 3: 生成视频标题**
- 调用 `generate_title()`
- 使用提示词模板 `title_generation.py`
- LLM 根据旁白内容生成吸引人的标题

**Step 4: 检测模板类型**
- 解析模板文件名判断类型：
  - `static_*`：静态模板（无需 AI 媒体生成）
  - `image_*`：需要 AI 生成图像
  - `video_*`：需要 AI 生成视频
- 根据类型决定是否跳过媒体生成步骤（优化性能）

**Step 5: 生成图像提示词**
- 调用 `generate_image_prompts()`
- 批量处理：分批调用 LLM（避免 token 限制）
- 重试机制：失败自动重试
- 使用提示词模板 `image_generation.py`
- 输出：每个分镜的 image_prompt 列表

**Step 6: 创建故事板 (Storyboard)**
```python
Storyboard:
  title: "视频标题"
  config: StoryboardConfig (media_width/height, n_storyboard, TTS 参数, 媒体工作流, 帧模板)
  frames: [
    StoryboardFrame: {
      index: 1,
      narration: "旁白文本",
      image_prompt: "图像生成提示词",
      duration: 0,  # 将由 TTS 决定
      ...
    },
    ...
  ]
  content_metadata: {title, author, subtitle, genre, summary, ...}
```

**Step 7: 逐帧处理 (核心循环)**

对每个 StoryboardFrame 调用 FrameProcessor：

```
帧 N 处理流程:
┌─────────────────────────────────────────────┐
│  Step 1/4: TTS 生成音频                      │
│  - 调用 TTSService(frame.narration)          │
│  - 输出: audio_path (MP3 文件)                │
│  - 记录: frame.duration = 音频时长            │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  Step 2/4: AI 生成媒体 (图像/视频)            │
│  - 如果是静态模板，跳过此步骤                  │
│  - 调用 MediaService(frame.image_prompt)     │
│  - 如果是视频工作流，传递音频时长作为目标时长   │
│  - 输出: media_result (image/video URL)       │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  Step 3/4: HTML 模板合成帧                   │
│  - 调用 HTMLFrameGenerator.generate_frame()  │
│  - 渲染模板: 标题 + 旁白文本 + 媒体文件       │
│  - 输出: composed_image_path (PNG)            │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  Step 4/4: 创建视频片段                       │
│  - 如果是视频媒体:                            │
│    • 透明图像叠加到视频                      │
│    • 合并音频到视频                          │
│  - 如果是图像媒体:                            │
│    • 静态图像 + 音频生成视频                  │
│  - 输出: video_segment_path (MP4)             │
└─────────────────────────────────────────────┘
```

**并行处理支持**：
- 当使用 RunningHub 工作流时，支持并发处理多个帧
- 通过 `asyncio.Semaphore` 控制并发数
- 配置项：`runninghub_concurrent_limit`

**Step 8: 拼接视频**
- 调用 `VideoService.concat_videos()`
- 将所有 `video_segment_path` 拼接为完整视频
- 支持添加背景音乐（BGM）

**Step 9: 添加背景音乐**
- 调用 `VideoService.add_bgm_to_video()`
- 背景音乐循环播放适配视频时长
- BGM 音量可配置

**Step 10: 持久化元数据**
- 保存 `metadata.json`：任务输入参数、配置、结果路径
- 保存 `storyboard.json`：完整故事板数据
- 更新 `.index.json`：任务索引
- 返回 `VideoGenerationResult`：video_path, duration, file_size

### 6.2 素材驱动视频生成流程 (AssetBasedPipeline)

用户上传自己的图片/视频素材，系统自动分析并生成营销视频。

#### 流程概览

```
用户上传素材 (图片/视频)
  ↓
分析每个素材 (生成文字描述)
  ↓
LLM 生成脚本并分配素材到场景
  ↓
创建故事板
  ↓
逐帧处理 (TTS → 使用用户素材 → HTML 合成 → 视频片段)
  ↓
拼接视频
  ↓
添加背景音乐
  ↓
输出最终视频
```

#### 详细步骤

**Step 1: 分析素材**
- 对每个上传的图片调用 `ImageAnalysisService`
- 对每个上传的视频调用 `VideoAnalysisService`
- 输出：每个素材的文字描述

**Step 2: LLM 生成脚本**
- 使用结构化输出（Pydantic 模型：VideoScript）
- LLM 根据素材描述和用户需求生成场景分配方案
- 输出：VideoScript 包含场景列表、每场景的旁白、时长、使用的素材索引

**Step 3: 创建故事板**
- 根据 VideoScript 创建 Storyboard
- 匹配资产到场景
- 支持多旁白 per 场景（自动拼接音频）

**Step 4-N: 后续流程**
- 与 StandardPipeline 相同（逐帧处理、拼接、添加 BGM）

### 6.3 自定义模板流程 (CustomPipeline)

使用自定义 HTML 模板和工作流生成视频。

#### 流程概览

```
用户提供内容 + 模板选择
  ↓
使用指定模板渲染
  ↓
调用自定义工作流
  ↓
生成视频
```

### 6.4 Web 端流水线

Web 前端支持 5 种 Pipeline UI（插件式架构）：

| Pipeline | 图标 | 功能 |
|----------|------|------|
| **快速创作** | ⚡ | 输入主题，AI 全自动生成 |
| **自定义素材** | 🎨 | 使用自有图片/视频素材生成 |
| **数字人口播** | 🤖 | 数字人口播视频 |
| **图生视频** | 🎥 | 图片+提示词生成视频 |
| **动作迁移** | 💃 | 图片+参考视频生成动作迁移视频 |

---

## 七、API 接口文档

### 7.1 API 概览

基础路径：`/api`

| 模块 | 路由前缀 | 功能 |
|------|---------|------|
| 健康检查 | `/health` | 服务状态检查 |
| LLM | `/llm` | 大语言模型调用 |
| TTS | `/tts` | 文字转语音合成 |
| 图像 | `/image` | AI 图像生成 |
| 内容 | `/content` | 内容生成（旁白/提示词/标题） |
| 视频 | `/video` | 视频生成（同步/异步） |
| 任务 | `/tasks` | 任务管理（查询/取消） |
| 文件 | `/files` | 文件访问服务 |
| 资源 | `/resources` | 资源发现（工作流/模板/BGM） |
| 帧 | `/frame` | 帧渲染 |

### 7.2 核心 API 端点

#### 健康检查

```
GET /health
GET /version
```

返回服务状态和版本信息。

#### 视频生成（同步）

```
POST /api/video/generate/sync
```

**请求体**（VideoGenerateRequest）：
```json
{
  "text": "输入主题或脚本",
  "mode": "generate|fixed",
  "title": "视频标题（可选）",
  "n_scenes": 5,
  "tts_workflow": "tts_edge.json",
  "tts_voice": "zh-CN-XiaoxiaoNeural",
  "llm_model": "qwen-plus",
  "media_workflow": "image_flux.json",
  "frame_template": "image_default.html",
  "bgm_path": "bgm/default.mp3",
  "media_width": 1080,
  "media_height": 1920
}
```

**响应**（VideoGenerateResponse）：
```json
{
  "video_url": "/api/files/output/{task_id}/final.mp4",
  "duration": 60.5,
  "file_size": 10240000
}
```

#### 视频生成（异步）

```
POST /api/video/generate/async
```

**响应**（VideoGenerateAsyncResponse）：
```json
{
  "task_id": "uuid-string"
}
```

#### 任务管理

```
GET    /api/tasks                     # 查询任务列表
GET    /api/tasks/{task_id}           # 查询任务详情
DELETE /api/tasks/{task_id}           # 删除任务
```

#### LLM 调用

```
POST /api/llm/chat
```

**请求体**（LLMChatRequest）：
```json
{
  "prompt": "你好，请写一段关于AI的介绍",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

#### TTS 合成

```
POST /api/tts/synthesize
```

**请求体**（TTSSynthesizeRequest）：
```json
{
  "text": "要合成的文本",
  "workflow": "tts_edge.json",
  "ref_audio": "参考音频URL（可选）",
  "voice_id": "音色ID"
}
```

#### 图像生成

```
POST /api/image/generate
```

**请求体**（ImageGenerateRequest）：
```json
{
  "prompt": "图像描述提示词",
  "width": 1080,
  "height": 1920,
  "workflow": "image_flux.json"
}
```

#### 内容生成

```
POST /api/content/narration       # 生成旁白
POST /api/content/image-prompt    # 生成图像提示词
POST /api/content/title           # 生成标题
```

#### 文件访问

```
GET /api/files/{file_path:path}
```

安全访问 output/, workflows/, templates/, bgm/, resources/ 目录下的文件。

#### 资源发现

```
GET /api/resources/workflows/tts       # 获取 TTS 工作流列表
GET /api/resources/workflows/media     # 获取媒体工作流列表
GET /api/resources/templates           # 获取 HTML 模板列表
GET /api/resources/bgm                 # 获取背景音乐列表
```

#### 帧渲染

```
POST /api/frame/render                 # 使用模板渲染单帧图像
GET  /api/frame/template/params        # 获取模板参数定义
```

---

## 八、前端架构

### 8.1 技术栈

- **Streamlit**：纯 Python 构建的交互式 Web 框架
- **组件化设计**：UI 组件按职责分离
- **插件式 Pipeline 架构**：通过注册表模式轻松添加新的视频生成工作流
- **国际化**：支持中英文自动切换

### 8.2 页面路由

```
web/app.py (主入口)
  ├── 🎬 Home (pages/1_🎬_Home.py)     # 默认页面 - 视频生成
  └── 📚 History (pages/2_📚_History.py)  # 历史记录页
```

### 8.3 Home 页面结构

```
Home Page
├── Header (页面标题 + 语言切换)
├── FAQ 侧边栏 (常见问题)
├── 高级设置 (可折叠)
│   ├── LLM 配置 (API Key / Base URL / Model)
│   └── ComfyUI 配置 (URL / RunningHub API Key)
└── Pipeline Tabs (Tab 式切换)
    ├── ⚡ 快速创作 (三栏布局)
    │   ├── 左栏: 内容输入 + BGM 选择
    │   ├── 中栏: 样式配置 (TTS / 模板 / 工作流)
    │   └── 右栏: 输出预览 + 生成按钮
    ├── 🎨 自定义素材
    ├── 🤖 数字人口播
    ├── 🎥 图生视频
    └── 💃 动作迁移
```

### 8.4 History 页面结构

```
History Page
├── Header
├── 侧边栏
│   ├── 统计指标 (完成/失败数)
│   ├── 状态筛选器
│   ├── 排序方式
│   └── 每页显示数量
└── 主内容区
    ├── [详情页模式] 任务详情模态框
    │   ├── 左列: 输入参数
    │   ├── 中列: 故事板分镜
    │   └── 右列: 最终视频预览
    └── [列表模式] 4列网格卡片
        ├── 视频预览
        ├── 标题 + 内容摘要
        ├── 元信息 (时间/时长/分镜数)
        └── 操作按钮 (查看/下载/删除)
    └── 分页控件
```

### 8.5 状态管理

采用 **Streamlit Session State** 管理状态：

```python
st.session_state.language                   # 当前语言
st.session_state.pixelle_video              # PixelleVideoCore 实例 (带缓存)
st.session_state.pixelle_video_config_hash  # 配置哈希 (检测变化)
st.session_state.llm_loaded_models          # 已加载的 LLM 模型列表
st.session_state.selected_template          # 选中的模板
st.session_state.history_page               # 历史分页状态
```

**核心优化**：通过配置哈希检测避免不必要的核心实例重建。

### 8.6 国际化 (i18n)

```python
# 翻译文件位置
web/i18n/locales/zh_CN.json   # 简体中文
web/i18n/locales/en_US.json   # 英语

# 使用方式
tr("app.title")                           # => "⚡ XiaoYu.AI - AI 全自动短视频引擎"
tr("status.video_generated", path=video)  # => 带参数插值
tr("faq.title", fallback="FAQ")           # 带后备值
```

**语言检测顺序**：
1. macOS: `defaults read -g AppleLocale`
2. 跨平台: `locale.getdefaultlocale()`
3. 环境变量: `LC_ALL`, `LANG`
4. 默认回退: 英语

---

## 九、配置说明

### 9.1 配置文件 (config.yaml)

```yaml
# 项目名称
project_name: "XiaoYu.AI"

# LLM 配置
llm:
  api_key: "your-api-key"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  model: "qwen-plus"

# ComfyUI 配置
comfyui:
  comfyui_url: "http://127.0.0.1:8188"
  comfyui_api_key: ""
  
  # RunningHub 配置
  runninghub_api_key: "your-runninghub-api-key"
  runninghub_concurrent_limit: 3
  runninghub_instance_type: ""
  
  # TTS 配置
  tts:
    inference_mode: "local"  # local / comfyui
    local:
      voice: "zh-CN-XiaoxiaoNeural"
    comfyui:
      default_workflow: "tts_edge.json"

  # 图像生成配置
  image:
    default_workflow: "image_flux.json"
    prompt_prefix: ""

  # 视频生成配置
  video:
    default_workflow: "video_wan2.1_fusionx.json"
    prompt_prefix: ""

# 模板配置
template:
  default_template: "image_default.html"
```

### 9.2 环境变量

系统也支持通过环境变量覆盖配置：

```bash
PIXELLE_LLM_API_KEY=your-api-key
PIXELLE_LLM_BASE_URL=https://api.openai.com/v1
PIXELLE_LLM_MODEL=gpt-4o
PIXELLE_COMFYUI_COMFYUI_URL=http://127.0.0.1:8188
PIXELLE_COMFYUI_RUNNINGHUB_API_KEY=your-key
```

### 9.3 ComfyKit 配置热重载

- ComfyKit 实例使用懒加载模式
- 配置变更自动检测（MD5 hash 比对）并重建实例
- 支持热重载配置，无需重启服务

---

## 十、部署方式

### 10.1 本地开发部署

#### 前置要求

- Python 3.11+
- uv (Python 包管理器)
- FFmpeg
- Chromium (用于 HTML 渲染)

#### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-org/Xiaoyu-Video.git
cd Xiaoyu-Video

# 2. 安装依赖
uv sync

# 3. 复制配置文件
cp config.example.yaml config.yaml
# 编辑 config.yaml 填入你的 API Key

# 4. 启动 Web UI
# Windows
start_web.bat

# Linux/Mac
./start_web.sh

# 或直接使用命令
uv run streamlit run web/app.py
```

访问 `http://localhost:8501` 即可使用 Web UI。

### 10.2 Docker 部署

#### 启动服务

```bash
# 使用提供的脚本
./docker-start.sh

# 或使用 docker-compose
docker-compose up -d
```

#### 服务说明

docker-compose.yml 定义了 3 个服务：

| 服务 | 端口 | 功能 |
|------|------|------|
| init | - | 初始化（创建数据目录） |
| api | 8000 | FastAPI 后端服务 |
| web | 8501 | Streamlit Web UI |

### 10.3 Windows 整合包

项目提供 Windows 整合包构建脚本：

```bash
cd packaging/windows
python build.py
```

生成的一键包包含所有依赖，可直接运行。

### 10.4 API 单独部署

如果只需要 API 服务：

```bash
# 启动 FastAPI 服务
uv run uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```

访问 API 文档：`http://localhost:8000/docs`

---

## 附录

### A. 关键设计模式

| 模式 | 应用场景 |
|------|---------|
| **依赖注入** | FastAPI `Depends` + 全局单例 |
| **模板方法模式** | LinearVideoPipeline 定义生命周期，子类覆盖步骤 |
| **策略模式** | 多种流水线（standard/custom/asset_based）可切换 |
| **懒加载** | ComfyKit 首次使用时创建，配置变更自动重建 |
| **热重载** | 配置动态读取，无需重启服务 |
| **并行处理** | asyncio.Semaphore 控制 RunningHub 并发 |
| **条件执行** | 根据模板类型跳过不需要的步骤 |
| **TTS 时长驱动** | 音频时长传递给视频工作流，确保音画同步 |
| **注册表模式** | Web Pipeline UI 插件式架构 |
| **文件系统持久化** | JSON 文件存储 + 索引加速查询 |

### B. 重要数据模型

#### Storyboard（故事板）

```python
@dataclass
class Storyboard:
    title: str                           # 视频标题
    config: StoryboardConfig             # 配置
    frames: List[StoryboardFrame]        # 分镜列表
    content_metadata: ContentMetadata    # 内容元数据
    final_video_path: str                # 最终视频路径
    total_duration: float                # 总时长
    created_at: datetime                 # 创建时间
    completed_at: datetime               # 完成时间
```

#### StoryboardFrame（分镜）

```python
@dataclass
class StoryboardFrame:
    index: int                           # 帧索引
    narration: str                       # 旁白文本
    image_prompt: str                    # 图像生成提示词
    audio_path: str                      # TTS 音频路径
    media_type: str                      # "image" 或 "video"
    image_path: str                      # AI 生成的图像路径
    video_path: str                      # AI 生成的视频路径
    composed_image_path: str             # HTML 合成的帧图像路径
    video_segment_path: str              # 视频片段路径
    duration: float                      # 时长（秒）
```

#### ProgressEvent（进度事件）

```python
@dataclass
class ProgressEvent:
    event_type: str                      # 事件类型
    progress: float                      # 0.0-1.0
    frame_current: int                   # 当前帧
    frame_total: int                     # 总帧数
    step: int                            # 帧内步骤 (1-4)
    action: str                          # 动作 (audio/media/compose/video)
    extra_info: str                      # 附加信息
```

### C. ComfyUI 工作流列表

#### RunningHub 云端工作流 (21个)

| 工作流 | 用途 |
|--------|------|
| af_scail | 智能裁剪 |
| analyse_image | 图像分析 |
| digital_combination | 数字人组合 |
| digital_customize | 数字人定制 |
| digital_image | 数字人图像 |
| i2v_LTX2 | LTX2 图生视频 |
| image_flux / image_flux2 | Flux 图像生成 |
| image_qwen / image_qwen_chinese_cartoon | Qwen 图像生成 |
| image_sd3.5 | SD3.5 图像生成 |
| image_sdxl | SDXL 图像生成 |
| image_Z-image | Z-image 生成 |
| tts_edge / tts_index2 / tts_spark | TTS 合成 |
| video_qwen_wan2.2 / video_wan2.1_fusionx / video_wan2.2 | 视频生成 |
| video_understanding | 视频理解 |
| video_Z_image_wan2.2 | Z-image 视频生成 |

#### Selfhost 本地工作流 (8个)

| 工作流 | 用途 |
|--------|------|
| analyse_image | 图像分析 |
| analyse_video | 视频分析 |
| image_flux | Flux 图像生成 |
| image_nano_banana | Nano Banana 图像生成 |
| image_qwen | Qwen 图像生成 |
| tts_edge | Edge TTS |
| tts_index2 | Index TTS |
| video_wan2.1_fusionx | Wan2.1 视频生成 |

### D. HTML 模板列表

#### 竖屏 1080x1920 (25个)

asset_default, image_blur_card, image_book, image_cartoon, image_default, 
image_elegant, image_excerpt, image_fashion_vintage, image_full, image_healing, 
image_health_preservation, image_life_insights_light, image_life_insights, 
image_long_text, image_modern, image_neon, image_psychology_card, image_purple, 
image_satirical_cartoon, image_simple_black, image_simple_line_drawing, 
static_default, static_excerpt, video_default, video_healing

#### 方形 1080x1080 (1个)

image_minimal_framed

#### 横屏 1920x1080 (5个)

image_book, image_film, image_full, image_ultrawide_minimal, image_wide_darktech

### E. 常见工作流

#### 典型视频生成流程（用户视角）

1. 访问 Web UI (`http://localhost:8501`)
2. 在「快速创作」Tab 输入主题（例如："AI 如何改变我们的生活"）
3. 选择样式配置：
   - TTS 音色：zh-CN-XiaoxiaoNeural
   - 帧模板：image_default.html
   - 媒体工作流：image_flux.json
4. 点击「生成视频」按钮
5. 观看实时进度条
6. 完成后预览并下载视频

#### 使用 API 生成视频

```bash
# 异步生成视频
curl -X POST http://localhost:8000/api/video/generate/async \
  -H "Content-Type: application/json" \
  -d '{
    "text": "AI 如何改变我们的生活",
    "n_scenes": 5,
    "tts_voice": "zh-CN-XiaoxiaoNeural",
    "frame_template": "image_default.html",
    "media_workflow": "image_flux.json"
  }'

# 返回: {"task_id": "uuid"}

# 查询任务状态
curl http://localhost:8000/api/tasks/{task_id}

# 下载视频
curl http://localhost:8000/api/files/output/{task_id}/final.mp4 --output video.mp4
```

---

## 总结

**XiaoYu.AI** 是一个功能强大的 AI 全自动短视频生成平台，具有以下特点：

✅ **简单易用**：输入主题即可生成完整视频  
✅ **模块化设计**：各服务模块职责清晰，易于扩展  
✅ **多模式支持**：AI 自动生成、素材驱动、数字人、图生视频、动作迁移  
✅ **高性能**：异步处理、并发控制、热重载配置  
✅ **灵活部署**：支持本地、Docker、Windows 整合包  
✅ **双服务源**：支持 RunningHub 云服务和自部署 ComfyUI  
✅ **完善文档**：中英双语文档、API 文档、FAQ  

**技术栈亮点**：
- FastAPI + Streamlit 全栈 Python
- ComfyKit 统一封装 ComfyUI/RunningHub
- FFmpeg 专业视频处理
- OpenAI SDK 兼容多家 LLM 提供商
- 插件式架构，轻松扩展新流水线

---

*文档生成时间：2026年4月8日*  
*项目版本：0.1.15*
