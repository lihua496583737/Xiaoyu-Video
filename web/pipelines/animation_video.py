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
Animation Video Pipeline UI for Streamlit Web interface
"""

import streamlit as st

from web.pipelines.base import PipelineUI, register_pipeline_ui
from web.i18n import tr


class AnimationVideoPipelineUI(PipelineUI):
    """Animation video generation pipeline UI"""
    
    name = "animation_video"
    icon = "🎬"
    
    @property
    def display_name(self):
        return tr("pipeline.animation_video.name", "AI 动画视频")
    
    @property
    def description(self):
        return tr(
            "pipeline.animation_video.description",
            "生成高质量动画视频，支持角色一致性、口型同步、电影级运镜"
        )
    
    def render(self, pixelle_video):
        """Render the animation video pipeline UI"""
        # Two-column layout: [2, 1]
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_character_config(pixelle_video)
            self._render_animation_script(pixelle_video)
            self._render_style_and_model(pixelle_video)
        
        with col2:
            self._render_cost_estimator(pixelle_video)
            self._render_output_preview(pixelle_video)
    
    def _render_character_config(self, pixelle_video):
        """Render character configuration"""
        with st.expander(tr("animation.character.title", "角色配置"), expanded=True):
            # Initialize characters in session state
            if "animation_characters" not in st.session_state:
                st.session_state.animation_characters = []
            
            characters = st.session_state.animation_characters
            
            # Add character button
            if st.button(tr("animation.character.add", "➕ 添加角色")):
                characters.append({
                    "name": "",
                    "description": "",
                    "tts_voice": "zh-CN-YunxiNeural",
                    "reference_images": [],
                })
            
            # Edit each character
            for i, char in enumerate(characters):
                with st.container():
                    st.markdown(f"**{tr('animation.character.index', '角色')} {i+1}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        char["name"] = st.text_input(
                            tr("animation.character.name", "角色名称"),
                            value=char.get("name", ""),
                            key=f"char_name_{i}",
                        )
                    with col_b:
                        char["tts_voice"] = st.selectbox(
                            tr("animation.character.voice", "TTS 音色"),
                            options=["zh-CN-YunxiNeural", "zh-CN-XiaoxiaoNeural", "zh-CN-YunjianNeural"],
                            index=["zh-CN-YunxiNeural", "zh-CN-XiaoxiaoNeural", "zh-CN-YunjianNeural"].index(char.get("tts_voice", "zh-CN-YunxiNeural")),
                            key=f"char_voice_{i}",
                        )
                    char["description"] = st.text_area(
                        tr("animation.character.description", "外观描述"),
                        value=char.get("description", ""),
                        key=f"char_desc_{i}",
                    )
                    
                    # Remove button
                    if st.button(tr("animation.character.remove", "🗑️ 删除"), key=f"remove_char_{i}"):
                        characters.pop(i)
                        st.rerun()
    
    def _render_animation_script(self, pixelle_video):
        """Render animation script input"""
        with st.expander(tr("animation.script.title", "动画脚本"), expanded=True):
            # Simple mode: topic input
            topic = st.text_area(
                tr("animation.script.topic", "主题"),
                placeholder=tr("animation.script.topic_placeholder", "例如：修仙少年成长故事"),
                height=100,
                key="animation_topic",
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                n_scenes = st.slider(
                    tr("animation.script.n_scenes", "场景数量"),
                    min_value=3,
                    max_value=8,
                    value=5,
                    key="animation_n_scenes",
                )
            with col_b:
                target_duration = st.slider(
                    tr("animation.script.duration", "目标时长（秒）"),
                    min_value=15,
                    max_value=120,
                    value=30,
                    step=5,
                    key="animation_duration",
                )
            
            if st.button(tr("animation.script.generate", "✨ 生成脚本")):
                st.info(tr("animation.script.generating", "脚本将在生成视频时自动创建"))
    
    def _render_style_and_model(self, pixelle_video):
        """Render style and model selection"""
        with st.expander(tr("animation.style.title", "动画风格"), expanded=True):
            style = st.selectbox(
                tr("animation.style.select", "选择风格"),
                options=[
                    "fanren_xianxia",
                    "douluo_dalu",
                    "demon_slayer",
                    "jujutsu_kaisen",
                    "disney_3d",
                    "watercolor",
                    "cyberpunk",
                    "children",
                ],
                format_func=lambda x: {
                    "fanren_xianxia": "凡人修仙传风格",
                    "douluo_dalu": "斗罗大陆风格",
                    "demon_slayer": "鬼灭之刃风格",
                    "jujutsu_kaisen": "咒术回战风格",
                    "disney_3d": "迪士尼3D风格",
                    "watercolor": "水墨风格",
                    "cyberpunk": "赛博朋克风格",
                    "children": "儿童动画风格",
                }.get(x, x),
                key="animation_style",
            )
        
        with st.expander(tr("animation.model.title", "视频生成模型"), expanded=False):
            model = st.selectbox(
                tr("animation.model.select", "选择模型"),
                options=["ltx2.3", "wan2.2", "kling2.6"],
                format_func=lambda x: {
                    "ltx2.3": "LTX 2.3（推荐）",
                    "wan2.2": "Wan2.2（电影感）",
                    "kling2.6": "Kling 2.6（最强一致性）",
                }.get(x, x),
                key="animation_model",
            )
            
            st.caption(tr("animation.model.description", "不同模型在质量、速度、成本上有所差异"))
        
        with st.expander(tr("animation.postprocess.title", "后期处理"), expanded=False):
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(tr("animation.postprocess.upscale", "视频超分（720p→1080p）"), value=True, key="animation_enable_upscale")
                st.checkbox(tr("animation.postprocess.interpolate", "帧插值（24fps→48fps）"), value=True, key="animation_enable_interpolation")
            with col_b:
                st.checkbox(tr("animation.postprocess.color_grade", "色彩校正"), value=True, key="animation_enable_color_grading")
                st.checkbox(tr("animation.postprocess.lip_sync", "口型同步"), value=True, key="animation_enable_lip_sync")
    
    def _render_cost_estimator(self, pixelle_video):
        """Render cost estimation"""
        st.subheader(tr("animation.cost.title", "💰 成本估算"))
        
        # Get values from session state
        n_scenes = st.session_state.get("animation_n_scenes", 5)
        model = st.session_state.get("animation_model", "ltx2.3")
        enable_upscale = st.session_state.get("animation_enable_upscale", True)
        enable_interpolation = st.session_state.get("animation_enable_interpolation", True)
        
        # Calculate cost (simplified)
        cost_per_scene = {"ltx2.3": 3.0, "wan2.2": 2.0, "kling2.6": 5.0}
        video_cost = n_scenes * cost_per_scene.get(model, 3.0)
        post_cost = 0
        if enable_upscale:
            post_cost += n_scenes * 0.5
        if enable_interpolation:
            post_cost += n_scenes * 0.5
        
        total_cost = video_cost + post_cost + 0.5  # Base costs
        
        st.metric(tr("animation.cost.total", "预估总成本"), f"¥{total_cost:.2f}")
        st.caption(tr("animation.cost.note", "实际成本可能因重试次数而有所变化"))
    
    def _render_output_preview(self, pixelle_video):
        """Render output preview and generation button"""
        st.subheader(tr("animation.output.title", "生成视频"))
        
        # Warning about time and cost
        st.warning(tr(
            "animation.hint.long_generation",
            "⚠️ 动画视频生成时间较长（30-90分钟），成本较高（10-50元），请确认后再开始"
        ))
        
        if st.button(
            tr("animation.btn.generate", "🚀 生成动画视频"),
            type="primary",
            use_container_width=True,
        ):
            # Validate inputs
            topic = st.session_state.get("animation_topic", "")
            if not topic:
                st.error(tr("animation.hint.no_topic", "请输入主题"))
                return
            
            st.session_state.animation_generating = True
            
            # Call backend pipeline
            try:
                from web.utils.async_helpers import run_async
                
                style = st.session_state.get("animation_style", "fanren_xianxia")
                model = st.session_state.get("animation_model", "ltx2.3")
                n_scenes = st.session_state.get("animation_n_scenes", 5)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(event):
                    progress = int(event.progress * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"{event.event_type}: {event.extra_info}")
                
                result = run_async(
                    pixelle_video.generate_video(
                        text=topic,
                        pipeline="animation",
                        animation_style=style,
                        video_model=model,
                        n_scenes=n_scenes,
                        progress_callback=update_progress,
                    )
                )
                
                progress_bar.progress(100)
                status_text.text(tr("animation.progress.completed", "生成完成！"))
                
                # Show result
                if result and hasattr(result, "video_path"):
                    st.success(tr("animation.output.success", "视频生成成功！"))
                    st.video(result.video_path)
                    
                    # Download button
                    with open(result.video_path, "rb") as f:
                        st.download_button(
                            label=tr("animation.btn.download", "⬇️ 下载视频"),
                            data=f,
                            file_name="animation_video.mp4",
                            mime="video/mp4",
                        )
                
            except Exception as e:
                st.error(tr("animation.error.generation_failed", f"生成失败：{str(e)}"))
            finally:
                st.session_state.animation_generating = False


# Register the pipeline UI
register_pipeline_ui(AnimationVideoPipelineUI)
