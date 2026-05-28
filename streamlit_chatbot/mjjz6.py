import streamlit as st
import json
import os
import random
from datetime import datetime, date
from PIL import Image
import pandas as pd
import plotly.express as px
import pytz

# ---------------------- 1. 登录系统配置 ----------------------
# 你可以在这里设置多个密码，比如自己用的、备用的
VALID_PASSWORDS = ["1234"] 

# 初始化session state，记录用户是否已登录
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 登录页面
def login_page():
    st.title("🔒 My Daily Journal")
    st.markdown("### Please Enter Your Password")
    
    password = st.text_input("密码", type="password")
    if st.button("登录", use_container_width=True):
        if password in VALID_PASSWORDS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("密码错误，请重试")

# 如果未登录，只显示登录页面
if not st.session_state.logged_in:
    login_page()
    st.stop()  # 停止执行后面的所有代码，保护隐私

# ---------------------- 2. 时区设置 ----------------------
tz = pytz.timezone("Asia/Kuala_Lumpur")  # 马来西亚时区，如需中国请改为"Asia/Shanghai"

# ---------------------- 3. App Configuration & 全局美化 ----------------------
st.set_page_config(
    page_title="MoodVibe Journal",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "MoodVibe Journal - Your personal life diary & mood tracker"
    }
)

# 全局CSS美化（温柔粉白渐变+圆角卡片+hover动画）
st.markdown("""
<style>
/* 全局背景 */
.stApp {
    background: linear-gradient(135deg, #fff5f7 0%, #ffeef8 100%);
    color: #333333;
}

/* 输入框美化 */
.stTextArea, .stTextInput {
    background-color: rgba(255,255,255,0.85) !important;
    border-radius: 12px !important;
    border: 1px solid #e0e0e0 !important;
}

/* 按钮美化 */
.stButton>button {
    background-color: #ffb6c1 !important;
    color: white !important;
    border-radius: 25px !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(255,182,193,0.3);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #ff9eb5 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(255,158,181,0.4);
}

/* 侧边栏美化 */
.css-1d391kg {
    background-color: rgba(255,255,255,0.9) !important;
    border-right: 1px solid #eee;
}

/* 卡片容器美化 */
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin: 10px 0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

/* 装饰分隔线 */
.divider {
    text-align: center;
    margin: 20px 0;
    color: #ffb6c1;
    font-size: 18px;
}

/* 标题渐变文字 */
h1, h2, h3 {
    background: linear-gradient(90deg, #ff9a9e, #fad0c4);
    -webkit-background-clip: text;
    color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- 4. Constants ----------------------
DATA_FILE = "journal_entries.json"
IMAGE_FOLDER = "journal_images"
MOOD_EMOJIS = {
    "😊 Happy": "😊",
    "😌 Calm": "😌",
    "🥰 Loved": "🥰",
    "😴 Tired": "😴",
    "😆 Excited": "😆",
    "🤔 Thoughtful": "🤔",
    "😔 Sad": "😔",
    "😤 Upset": "😤",
    "✨ Blessed": "✨",
    "😰 Anxious": "😰",
    "😡 Angry": "😡"
}

POSITIVE_QUOTES = [
    "Every day is a new beginning. Embrace it fully.",
    "Your only limit is the one you set yourself.",
    "Small steps create big dreams. Keep going.",
    "Be proud of how far you have come.",
    "Happiness comes from within, not from others.",
    "Today is full of endless possibilities.",
    "You are stronger than you think.",
    "Cherish every little moment in life.",
    "Smile, the world needs your light.",
    "Trust the process, everything will be fine.",
    "Your future self will thank you for today.",
    "Growth happens outside your comfort zone.",
    "Be kind to yourself. You're doing your best."
]

# ---------------------- 5. Helper Functions ----------------------
def init_app():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

def load_entries():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_entry(entry):
    entries = load_entries()
    entries.append(entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def delete_entry(index):
    entries = load_entries()
    if 0 <= index < len(entries):
        if entries[index]["image_path"] and os.path.exists(entries[index]["image_path"]):
            os.remove(entries[index]["image_path"])
        del entries[index]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        return True
    return False

def compress_and_save_image(uploaded_img):
    if uploaded_img is None:
        return ""
    img = Image.open(uploaded_img)
    img.thumbnail((1024, 1024))
    timestamp = datetime.now(tz).strftime("%Y%m%d%H%M%S")
    img_path = os.path.join(IMAGE_FOLDER, f"img_{timestamp}.png")
    img.save(img_path, "PNG", quality=85)
    return img_path

def get_mood_stats(entries):
    if not entries:
        return None
    mood_counts = {}
    for entry in entries:
        mood = entry["mood"]
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    return pd.DataFrame(list(mood_counts.items()), columns=["Mood", "Count"])

# ---------------------- 6. Initialize App ----------------------
init_app()

# ---------------------- 7. Sidebar ----------------------
with st.sidebar:
    st.header("📖 MoodVibe Journal")
    st.markdown("---")
    
    nav = st.radio(
        "Navigation",
        ["✍️ Write New Entry", "📚 View & Manage Journals", "📊 Mood Statistics", "💾 Data Tools"]
    )
    
    st.markdown("---")
    # 退出登录按钮
    if st.button("退出登录", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    
    st.caption("✨ Your Personal Life Diary & Mood Tracker")
    st.caption("Built with ❤️ using Streamlit")

# ---------------------- 8. Page 1: Write New Entry ----------------------
if nav == "✍️ Write New Entry":
    st.header("🌸 Today's Entry 🌸")
    st.markdown('<div class="divider">✨ ✨ ✨ ✨ ✨</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("How are you feeling today?")
        
        selected_mood = st.selectbox("Choose your mood", list(MOOD_EMOJIS.keys()))
        mood_emoji = MOOD_EMOJIS[selected_mood]
        st.info(f"Current Mood: {mood_emoji} {selected_mood}")
        
        journal_content = st.text_area(
            "Write your thoughts, stories, or daily moments:",
            height=250,
            placeholder="What happened today? How did it make you feel?"
        )
        
        tags = st.text_input("Add tags (comma separated, optional)", placeholder="e.g., happy, work, family")
    
    with col2:
        st.subheader("Add a Photo 📸")
        uploaded_img = st.file_uploader("Upload a photo (optional)", type=["jpg", "jpeg", "png"])
        
        if uploaded_img is not None:
            img = Image.open(uploaded_img)
            st.image(img, caption="Preview", use_column_width=True)
        else:
            st.info("No photo uploaded yet")
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💫 Daily Positive Quote")
        daily_quote = random.choice(POSITIVE_QUOTES)
        st.success(f'"{daily_quote}"')
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("💾 Save Entry", type="primary", use_container_width=True):
        if not journal_content.strip():
            st.warning("Please write something in your journal before saving!")
        else:
            img_path = compress_and_save_image(uploaded_img)
            
            new_entry = {
                "timestamp": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
                "date": datetime.now(tz).date().isoformat(),
                "mood": selected_mood,
                "emoji": mood_emoji,
                "content": journal_content,
                "tags": [tag.strip() for tag in tags.split(",")] if tags else [],
                "image_path": img_path
            }
            
            save_entry(new_entry)
            st.success("✅ Your journal entry has been saved successfully!")
            st.balloons()

# ---------------------- 9. Page 2: View & Manage Journals ----------------------
elif nav == "📚 View & Manage Journals":
    st.header("📚 Your Journal History")
    st.markdown('<div class="divider">✨ ✨ ✨ ✨ ✨</div>', unsafe_allow_html=True)
    
    entries = load_entries()
    if not entries:
        st.info("No journal entries yet. Start writing your first moment!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            filter_mood = st.selectbox("Filter by mood", ["All"] + list(MOOD_EMOJIS.keys()))
        with col2:
            filter_date = st.date_input("Filter by date", value=None)
        
        filtered_entries = entries.copy()
        if filter_mood != "All":
            filtered_entries = [e for e in filtered_entries if e["mood"] == filter_mood]
        if filter_date:
            filtered_entries = [e for e in filtered_entries if e["date"] == filter_date.isoformat()]
        
        if not filtered_entries:
            st.info("No entries match your filters.")
        else:
            for idx, entry in enumerate(reversed(filtered_entries)):
                original_idx = len(entries) - 1 - idx
                with st.expander(f"{entry['timestamp']} | {entry['emoji']} {entry['mood']}"):
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.write(entry["content"])
                    
                    if entry["tags"]:
                        st.markdown(f"Tags: {', '.join([f'`{tag}`' for tag in entry['tags']])}")
                    
                    if entry["image_path"] and os.path.exists(entry["image_path"]):
                        st.image(entry["image_path"], use_column_width=True)
                    
                    if st.button("🗑️ Delete Entry", key=f"del_{original_idx}", type="secondary"):
                        if delete_entry(original_idx):
                            st.success("Entry deleted successfully!")
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- 10. Page 3: Mood Statistics ----------------------
elif nav == "📊 Mood Statistics":
    st.header("📊 Your Mood Overview")
    st.markdown('<div class="divider">✨ ✨ ✨ ✨ ✨</div>', unsafe_allow_html=True)
    
    entries = load_entries()
    if not entries:
        st.info("No journal entries yet. Write some entries to see your mood statistics!")
    else:
        total_entries = len(entries)
        mood_stats = get_mood_stats(entries)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Entries", total_entries)
        with col2:
            most_common_mood = mood_stats.loc[mood_stats["Count"].idxmax(), "Mood"]
            st.metric("Most Common Mood", f"{MOOD_EMOJIS[most_common_mood]} {most_common_mood}")
        with col3:
            recent_entries = len([e for e in entries if (datetime.now(tz) - datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz)).days <= 7])
            st.metric("Entries This Week", recent_entries)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Word Cloud of Your Thoughts")
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        all_text = " ".join([entry["content"] for entry in entries])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Mood Distribution")
        fig = px.bar(
            mood_stats,
            x="Mood",
            y="Count",
            color="Mood",
            color_discrete_map={mood: color for mood, color in zip(MOOD_EMOJIS.keys(), ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#F1948A", "#85C1E9"])}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Mood Timeline")
        df = pd.DataFrame(entries)
        df["datetime"] = pd.to_datetime(df["timestamp"])
        df["mood_code"] = df["mood"].map({mood: i for i, mood in enumerate(MOOD_EMOJIS.keys())})
        
        fig = px.scatter(
            df,
            x="datetime",
            y="mood_code",
            color="mood",
            hover_data=["content", "tags"],
            labels={"datetime": "Date", "mood_code": "Mood"},
            color_discrete_map={mood: color for mood, color in zip(MOOD_EMOJIS.keys(), ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#F1948A", "#85C1E9"])}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- 11. Page 4: Data Tools ----------------------
elif nav == "💾 Data Tools":
    st.header("💾 Data Management")
    st.markdown('<div class="divider">✨ ✨ ✨ ✨ ✨</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Export Your Data")
    entries = load_entries()
    if entries:
        json_data = json.dumps(entries, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Download All Entries (JSON)",
            data=json_data,
            file_name="journal_backup.json",
            mime="application/json"
        )
        
        df = pd.DataFrame(entries)
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Entries (CSV)",
            data=csv_data,
            file_name="journal_backup.csv",
            mime="text/csv"
        )
    else:
        st.info("No data to export yet.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Import Data (Advanced)")
    st.warning("⚠️ This will merge imported data with existing entries. Make sure you have a backup first!")
    uploaded_backup = st.file_uploader("Upload a journal_backup.json file", type=["json"])
    if uploaded_backup is not None:
        if st.button("📤 Import Data", type="secondary"):
            try:
                imported_data = json.load(uploaded_backup)
                existing_data = load_entries()
                combined_data = existing_data + imported_data
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(combined_data, f, ensure_ascii=False, indent=2)
                st.success("Data imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing data: {e}")
    st.markdown('</div>', unsafe_allow_html=True)