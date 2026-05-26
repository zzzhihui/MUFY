import streamlit as st
import json
import os
from PIL import Image
from datetime import datetime

# ---------------------- App Basic Config & Name ----------------------
# Website Name: **MoodVibe Journal** (Creative, English, fits theme)
st.set_page_config(
    page_title="MoodVibe Journal",
    page_icon="📔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global file for saving journal data
DATA_FILE = "journal_data.json"

# ---------------------- Data Initialization ----------------------
def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def load_journals():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_journal(entry):
    journals = load_journals()
    journals.append(entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(journals, f, ensure_ascii=False, indent=2)

init_data()

# ---------------------- Mood Emoji List ----------------------
MOOD_EMOJIS = {
    "😊 Happy": "😊",
    "😌 Calm": "😌",
    "🥰 Loved": "🥰",
    "😴 Tired": "😴",
    "😆 Excited": "😆",
    "🤔 Thoughtful": "🤔",
    "😔 Sad": "😔",
    "😤 Upset": "😤",
    "✨ Blessed": "✨"
}

# ---------------------- Positive Quotes Library (Auto Generate) ----------------------
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
    "Trust the process, everything will be fine."
]

# ---------------------- UI Header ----------------------
st.markdown("""
# 📔 MoodVibe Journal
### Your Personal Life Diary | Record Moments • Share Moods • Get Positive Vibes
---
""")

# Split page into 2 columns
col1, col2 = st.columns([1.2, 1])

# ===================== LEFT COLUMN: Write New Journal =====================
with col1:
    st.subheader("✍️ Write Today's Journal")
    
    # 1. Mood Select (Emoji)
    selected_mood = st.selectbox("How do you feel today?", list(MOOD_EMOJIS.keys()))
    mood_emoji = MOOD_EMOJIS[selected_mood]
    st.info(f"Current Mood: {mood_emoji} {selected_mood}")

    # 2. Journal Text Input
    journal_content = st.text_area("Write your story, thoughts or daily moments here:", height=200)

    # 3. Photo Upload
    uploaded_img = st.file_uploader("📷 Upload your daily photo", type=["jpg", "jpeg", "png"])
    img_path = ""
    if uploaded_img is not None:
        img = Image.open(uploaded_img)
        st.image(img, caption="Preview Photo", use_column_width=True)
        # Save image locally
        img_name = f"img_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        img.save(img_name)
        img_path = img_name

    # 4. Save Button
    if st.button("💾 Save This Journal", type="primary"):
        if journal_content.strip() == "":
            st.warning("Please write something before saving!")
        else:
            new_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "mood": selected_mood,
                "emoji": mood_emoji,
                "content": journal_content,
                "image": img_path
            }
            save_journal(new_entry)
            st.success("✅ Journal saved successfully!")

# ===================== RIGHT COLUMN: Quotes & Journal History =====================
with col2:
    st.subheader("💫 Daily Positive Quote")
    # Auto random quote
    import random
    daily_quote = random.choice(POSITIVE_QUOTES)
    st.success(f"\"{daily_quote}\"")

    st.markdown("---")
    st.subheader("📚 Your Journal History")

    # Load & show all history
    all_entries = load_journals()
    if len(all_entries) == 0:
        st.info("No journal entries yet. Start writing your first moment!")
    else:
        # Reverse to show latest first
        for entry in reversed(all_entries):
            with st.expander(f"{entry['date']} | {entry['emoji']} {entry['mood']}"):
                st.write(entry["content"])
                if entry["image"] and os.path.exists(entry["image"]):
                    st.image(entry["image"], use_column_width=True)

# ---------------------- Sidebar Guide ----------------------
with st.sidebar:
    st.header("📖 App Guide")
    st.write("1. Select your mood with emoji")
    st.write("2. Write your daily journal")
    st.write("3. Upload favorite photos")
    st.write("4. Click Save to record")
    st.write("5. Get random positive quotes every time")
    st.divider()
    st.caption("MoodVibe Journal © Record your beautiful life")
