import streamlit as st
import random
from datetime import datetime

# ===================== 全局配置 & 样式动画 =====================
st.set_page_config(
    page_title="My Journal Space",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 动态CSS：动画、配色、黑白/彩色模式、全局样式
custom_css = """
<style>
/* 页面入场动画 */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
.main .block-container {
    animation: fadeIn 0.8s ease-in-out;
    padding-top: 2rem;
}

/* 彩色模式样式 */
.color-mode {
    background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
}
.color-mode h1, .color-mode h2, .color-mode h3 {
    color: #2c3e50;
}
.color-mode .stButton>button {
    background: #74b9ff;
    color: white;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}
.color-mode .stButton>button:hover {
    background: #0984e3;
    transform: scale(1.03);
}

/* 黑白(暗黑)模式样式 */
.dark-mode {
    background: #121212;
}
.dark-mode h1, .dark-mode h2, .dark-mode h3, .dark-mode p {
    color: #f1f1f1;
}
.dark-mode .stButton>button {
    background: #636e72;
    color: white;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}
.dark-mode .stButton>button:hover {
    background: #2d3436;
    transform: scale(1.03);
}

/* 心情标签动画 */
.emoji-tag {
    display: inline-block;
    font-size: 22px;
    margin: 4px;
    padding: 6px 10px;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s;
}
.emoji-tag:hover {
    transform: scale(1.15);
}

/* 语录卡片 */
.quote-card {
    padding: 1.2rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    animation: fadeIn 1s;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ===================== 数据初始化 =====================
# 励志语录库 (Positive Quotes)
QUOTE_LIST = [
    "Every day is a new beginning. Take a deep breath and start again.",
    "Your only limit is the one you set yourself.",
    "Small steps every day lead to big dreams.",
    "Believe in yourself and all that you are.",
    "Challenges make you stronger, don't give up.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "Stay positive, work hard and make it happen.",
    "You are capable of amazing things."
]

# 心情Emoji 分类
MOOD_EMOJI = {
    "Happy": "😊 😄 🥳 ✨",
    "Calm": "😌 🧘 ☁️ 🎧",
    "Tired": "😴 🥱 💤",
    "Excited": "🤩 🎉 💫",
    "Sad": "😔 💔 🌧️",
    "Motivated": "💪 🔥 🚀"
}

# 会话状态存储日记数据
if "journal_data" not in st.session_state:
    st.session_state.journal_data = []
if "mood_selected" not in st.session_state:
    st.session_state.mood_selected = ""
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ===================== 模式切换 =====================
def toggle_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# 应用页面主题
if st.session_state.dark_mode:
    st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
else:
    st.markdown('<div class="color-mode">', unsafe_allow_html=True)

# ===================== 侧边栏 =====================
with st.sidebar:
    st.title("📓 Journal Space")
    st.divider()

    # 黑白/彩色模式切换
    mode_text = "Switch to Color Mode" if st.session_state.dark_mode else "Switch to Dark Mode"
    st.button(mode_text, on_click=toggle_mode)

    st.divider()
    st.subheader("💭 Today's Mood")
    # 心情Emoji选择
    for mood, emojis in MOOD_EMOJI.items():
        if st.button(f"{mood} | {emojis}"):
            st.session_state.mood_selected = f"{mood}: {emojis}"

    st.divider()
    st.subheader("✨ Daily Positive Quote")
    # 自动随机生成励志语录
    random_quote = random.choice(QUOTE_LIST)
    st.markdown(f'<div class="quote-card">"{random_quote}"</div>', unsafe_allow_html=True)

# ===================== 主页面：日记功能 =====================
st.title("📒 My Daily Journal")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
st.subheader(f"Record Time: {current_time}")
st.divider()

# 1. 日记文本输入
journal_content = st.text_area(
    "Write your journal here...",
    height=200,
    placeholder="Share your day, thoughts and stories..."
)

# 2. 文件上传：图片 + 音频
col1, col2 = st.columns(2)
with col1:
    st.subheader("🖼️ Upload Photos")
    img_file = st.file_uploader("Choose image file", type=["png", "jpg", "jpeg"])
    if img_file is not None:
        st.image(img_file, use_column_width=True)

with col2:
    st.subheader("🎵 Upload Audio")
    audio_file = st.file_uploader("Choose audio file", type=["mp3", "wav"])
    if audio_file is not None:
        st.audio(audio_file, format="audio/mp3")

# 3. 保存日记
if st.button("💾 Save Today's Journal"):
    if journal_content.strip() or st.session_state.mood_selected:
        new_entry = {
            "time": current_time,
            "mood": st.session_state.mood_selected,
            "content": journal_content
        }
        st.session_state.journal_data.append(new_entry)
        st.success("✅ Journal saved successfully!")
    else:
        st.warning("⚠️ Please write something or select your mood first!")

st.divider()

# 4. 历史日记查看
st.subheader("📜 Past Journals")
if len(st.session_state.journal_data) == 0:
    st.info("No journal records yet. Start writing your first journal!")
else:
    for idx, entry in enumerate(reversed(st.session_state.journal_data)):
        with st.expander(f"Entry #{len(st.session_state.journal_data)-idx} | {entry['time']}"):
            st.write(f"**Mood:** {entry['mood']}")
            st.write(f"**Content:**\n{entry['content']}")

# 关闭主题div
st.markdown("</div>", unsafe_allow_html=True)