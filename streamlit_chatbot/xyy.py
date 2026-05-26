import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="Secret Journal",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 【核心样式：复刻周斯越清冷文艺风格】
custom_css = """
<style>
/* 全局淡入动画 轻柔版 */
@keyframes softFade {
    from {opacity: 0;}
    to {opacity: 1;}
}
.main .block-container {
    animation: softFade 1.2s ease-in-out;
    padding: 3rem 5rem;
    max-width: 1000px;
    margin: 0 auto;
}

/* 彩色模式：浅素色 原著温柔底色 */
.light-theme {
    background-color: #f8f9fa;
}
.light-theme h1, .light-theme h2, .light-theme h3 {
    color: #2c313a;
    font-weight: 400;
    letter-spacing: 1px;
}
.light-theme p, .light-theme label {
    color: #4a4f58;
}
.light-theme .stButton>button {
    background: #d1d9e6;
    color: #2c313a;
    border: none;
    border-radius: 6px;
    transition: all 0.25s ease;
}
.light-theme .stButton>button:hover {
    background: #b8c4d8;
}

/* 黑白/暗模式：复古静谧黑白色调 */
.dark-theme {
    background-color: #1a1a1a;
}
.dark-theme h1, .dark-theme h2, .dark-theme h3, .dark-theme p, .dark-theme label {
    color: #e2e2e2;
}
.dark-theme .stButton>button {
    background: #444444;
    color: #eeeeee;
    border: none;
    border-radius: 6px;
    transition: all 0.25s ease;
}
.dark-theme .stButton>button:hover {
    background: #5c5c5c;
}

/* 心情Emoji 简约标签 */
.mood-emoji {
    font-size: 20px;
    padding: 4px 8px;
    margin: 3px;
    border-radius: 4px;
    display: inline-block;
    transition: transform 0.2s;
}
.mood-emoji:hover {
    transform: translateY(-2px);
}

/* 语录卡片 简约卡片样式 */
.quote-box {
    padding: 1rem;
    border-left: 3px solid #94a3b8;
    margin: 1.5rem 0;
    font-style: italic;
}

/* 输入框统一简约风格 */
.stTextArea textarea {
    border-radius: 6px;
    border: 1px solid #ddd;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 数据素材
QUOTES = [
    "There is glory ahead.",
    "Quiet days are also worth cherishing.",
    "Keep going, the best is yet to come.",
    "Warmth always stays beside you.",
    "Every ordinary moment is unique."
]

MOOD_LIST = {
    "Peaceful": "☁️ 🕊️",
    "Joyful": "🌷 ✨",
    "Soft": "🌙 🎐",
    "Thoughtful": "📖 🪐",
    "Tender": "💌 🧸",
    "Hopeful": "🌟 🚶"
}

# 会话状态
if "journal_records" not in st.session_state:
    st.session_state.journal_records = []
if "current_mood" not in st.session_state:
    st.session_state.current_mood = ""
if "is_dark" not in st.session_state:
    st.session_state.is_dark = False

# 切换主题
def switch_theme():
    st.session_state.is_dark = not st.session_state.is_dark

# 加载主题容器
if st.session_state.is_dark:
    st.markdown('<div class="dark-theme">', unsafe_allow_html=True)
else:
    st.markdown('<div class="light-theme">', unsafe_allow_html=True)

# 页面标题（贴合原著私密日记感）
st.title("Secret Journal")
st.caption("A quiet space for daily thoughts and memories")
st.divider()

# 顶部：主题切换 + 当日语录
col_top1, col_top2 = st.columns([1, 3])
with col_top1:
    btn_text = "Light Mode" if st.session_state.is_dark else "Dark Mode"
    st.button(btn_text, on_click=switch_theme)

with col_top2:
    daily_quote = random.choice(QUOTES)
    st.markdown(f'<div class="quote-box">"{daily_quote}"</div>', unsafe_allow_html=True)

st.divider()

# 选择今日心情
st.subheader("Today's Mood")
mood_choose = ""
for name, emoji in MOOD_LIST.items():
    if st.button(f"{name}  {emoji}", key=name):
        st.session_state.current_mood = f"{name} {emoji}"

if st.session_state.current_mood:
    st.markdown(f"Selected: <span class='mood-emoji'>{st.session_state.current_mood}</span>", unsafe_allow_html=True)

st.divider()

# 日记正文输入
st.subheader("Write Your Journal")
now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
st.write(f"Time: {now_time}")
journal_text = st.text_area("", height=220, placeholder="Write down your day...")

# 图片 & 音频上传
col_up1, col_up2 = st.columns(2)
with col_up1:
    st.subheader("Attach Photo")
    img_upload = st.file_uploader("", type=["jpg","png","jpeg"])
    if img_upload:
        st.image(img_upload, width=300)

with col_up2:
    st.subheader("Attach Audio")
    audio_upload = st.file_uploader("", type=["mp3","wav"])
    if audio_upload:
        st.audio(audio_upload)

# 保存日记
if st.button("Save Journal"):
    if journal_text.strip() or st.session_state.current_mood:
        entry = {
            "time": now_time,
            "mood": st.session_state.current_mood,
            "content": journal_text
        }
        st.session_state.journal_records.append(entry)
        st.success("Saved successfully.")
    else:
        st.warning("Please write something or pick a mood.")

st.divider()

# 历史日记记录
st.subheader("Past Entries")
if not st.session_state.journal_records:
    st.info("No records yet. Start your first note.")
else:
    for idx, item in enumerate(reversed(st.session_state.journal_records)):
        with st.expander(f"Record {len(st.session_state.journal_records)-idx} | {item['time']}"):
            st.write(f"Mood: {item['mood']}")
            st.write(f"Content:\n{item['content']}")

# 关闭主题容器
st.markdown("</div>", unsafe_allow_html=True)