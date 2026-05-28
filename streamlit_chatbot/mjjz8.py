import streamlit as st
import json
import os
import random
from datetime import datetime, date
from PIL import Image
import pandas as pd
import plotly.express as px
import pytz

# ====================== 基础设置 ======================
# 存储所有用户账号信息的文件
ACCOUNTS_FILE = "accounts.json"
# 每个用户数据的根目录
BASE_DATA_FOLDER = "user_data"

# 初始化文件/文件夹
if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)
if not os.path.exists(BASE_DATA_FOLDER):
    os.makedirs(BASE_DATA_FOLDER)

# 加载所有账号
def load_accounts():
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 保存新账号
def save_account(username, password):
    accounts = load_accounts()
    accounts[username] = password
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)

# 初始化 session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ====================== 登录/注册页面 ======================
def auth_page():
    st.title("🌟 Student Wellness App")
    option = st.selectbox("Choose Option", ["Sign In", "Sign Up"])

    if option == "Sign Up":
        st.subheader("📝 Create Account")
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up", use_container_width=True):
            accounts = load_accounts()
            if new_username in accounts:
                st.error("Username already exists! Please choose another one.")
            elif new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 4:
                st.error("Password must be at least 4 characters!")
            else:
                save_account(new_username, new_password)
                # 创建用户专属文件夹
                os.makedirs(os.path.join(BASE_DATA_FOLDER, f"{new_username}_images"), exist_ok=True)
                with open(os.path.join(BASE_DATA_FOLDER, f"{new_username}_journal.json"), "w", encoding="utf-8") as f:
                    json.dump([], f)
                st.success("Account created successfully! Please Sign In now.")

    elif option == "Sign In":
        st.subheader("🔐 Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In", use_container_width=True):
            accounts = load_accounts()
            if username in accounts and accounts[username] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("Invalid username or password!")

# 未登录则只显示认证页面
if not st.session_state.logged_in:
    auth_page()
    st.stop()

# ====================== 时区设置 ======================
tz = pytz.timezone("Asia/Kuala_Lumpur")

# 获取当前用户的专属文件路径
current_user = st.session_state.current_user
user_json_path = os.path.join(BASE_DATA_FOLDER, f"{current_user}_journal.json")
user_img_folder = os.path.join(BASE_DATA_FOLDER, f"{current_user}_images")

# ====================== 全局美化样式 ======================
st.set_page_config(
    page_title="Student Wellness Journal",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff5f7 0%, #ffeef8 100%);
    color: #333333;
}
.stTextArea, .stTextInput {
    background-color: rgba(255,255,255,0.85) !important;
    border-radius: 12px !important;
    border: 1px solid #e0e0e0 !important;
}
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
.css-1d391kg {
    background-color: rgba(255,255,255,0.9) !important;
    border-right: 1px solid #eee;
}
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
.divider {
    text-align: center;
    margin: 20px 0;
    color: #ffb6c1;
    font-size: 18px;
}
h1, h2, h3 {
    background: linear-gradient(90deg, #ff9a9e, #fad0c4);
    -webkit-background-clip: text;
    color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ====================== 常量定义 ======================
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

# ====================== 工具函数 ======================
def load_entries():
    if not os.path.exists(user_json_path):
        with open(user_json_path, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(user_json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_entry(entry):
    entries = load_entries()
    entries.append(entry)
    with open(user_json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def delete_entry(index):
    entries = load_entries()
    if 0 <= index < len(entries):
        if entries[index]["image_path"] and os.path.exists(entries[index]["image_path"]):
            os.remove(entries[index]["image_path"])
        del entries[index]
        with open(user_json_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        return True
    return False

def compress_and_save_image(uploaded_img):
    if uploaded_img is None:
        return ""
    img = Image.open(uploaded_img)
    img.thumbnail((1024, 1024))
    timestamp = datetime.now(tz).strftime("%Y%m%d%H%M%S")
    img_path = os.path.join(user_img_folder, f"img_{timestamp}.png")
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

# ====================== 侧边栏 ======================
with st.sidebar:
    st.header("🌟 Student Wellness App")
    st.info(f"Welcome, {current_user}")
    st.markdown("---")

    nav = st.radio(
        "Navigation",
        ["✍️ Write New Entry", "📚 View & Manage Journals", "📊 Mood Statistics", "💾 Data Tools"]
    )

    st.markdown("---")
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

    st.caption("✨ Your Personal Wellness Journal")
    st.caption("Built with ❤️ using Streamlit")

# ====================== 主页面1：写日记 ======================
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
            st.warning("Please write something before saving!")
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
            st.success("✅ Entry saved successfully!")
            st.balloons()

# ====================== 主页面2：查看日记 ======================
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

# ====================== 主页面3：心情统计 ======================
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
            recent_entries = len([
                e for e in entries
                if (datetime.now(tz) - datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz)).days <= 7
            ])
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
            color_discrete_map={mood: color for mood, color in zip(
                MOOD_EMOJIS.keys(),
                ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#F1948A", "#85C1E9"]
            )}
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
            color_discrete_map={mood: color for mood, color in zip(
                MOOD_EMOJIS.keys(),
                ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#F1948A", "#85C1E9"]
            )}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ====================== 主页面4：数据工具 ======================
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
    st.warning("⚠️ This will merge imported data with existing entries. Please back up first!")
    uploaded_backup = st.file_uploader("Upload a journal_backup.json file", type=["json"])
    if uploaded_backup is not None:
        if st.button("📤 Import Data", type="secondary"):
            try:
                imported_data = json.load(uploaded_backup)
                existing_data = load_entries()
                combined_data = existing_data + imported_data
                with open(user_json_path, "w", encoding="utf-8") as f:
                    json.dump(combined_data, f, ensure_ascii=False, indent=2)
                st.success("Data imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Import failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.sidebar.title("🎧 Focus Music")


music_choice = st.sidebar.selectbox(
    "Choose music mood",
    ["None", "🌿 Calm", "😊 Happy", "✨ Satisfying"]
)




# =====================================================
# MUSIC LINKS (SIMPLE & SAFE)
# =====================================================


music_links = {
    "🌿 Calm": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "😊 Happy": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "✨ Satisfying": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
}




if music_choice != "None":


    st.sidebar.success(f"Playing: {music_choice}")


    st.audio(music_links[music_choice])

