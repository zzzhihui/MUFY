import streamlit as st
import random

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="BrightMind",
    page_icon="🌸",
    layout="centered"
)

# =========================
# CUSTOM CSS DESIGN
# =========================

st.markdown(
    """
    <style>

    .main {
        background-color: #fdf6ff;
    }

    .title {
        text-align: center;
        color: #a855f7;
        font-size: 50px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 40px;
    }

    .quote-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    .journal-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# POSITIVE QUOTES
# =========================

quotes = [

    "Small progress is still progress.",

    "You are stronger than you think.",

    "Believe in yourself.",

    "Every step forward matters.",

    "Stay patient. Your time will come.",

    "One good day can change everything."

]

# =========================
# WEBSITE TITLE
# =========================

st.markdown(
    '<div class="title">BrightMind 🌸</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Daily Positive Space</div>',
    unsafe_allow_html=True
)

# =========================
# RANDOM QUOTE SECTION
# =========================

st.markdown(
    '<div class="quote-box">',
    unsafe_allow_html=True
)

st.subheader("✨ Daily Positive Quote")

# Button generates quote
if st.button("Generate Quote"):

    random_quote = random.choice(quotes)

    st.success(random_quote)

else:

    st.info("Click the button for positivity 🌸")

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# =========================
# JOURNAL SECTION
# =========================

st.markdown(
    '<div class="journal-box">',
    unsafe_allow_html=True
)

st.subheader("📝 Mini Journal")

journal = st.text_area(
    "Write something positive today:",
    height=150
)

# Save button
if st.button("Save Journal"):

    st.success("Journal saved successfully!")

    st.write("Your journal entry:")
    st.write(journal)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# =========================
# FOOTER
# =========================

st.write("")
st.write("Made with positivity ✨")

# =====================================
# AI CHAT SECTION
# =====================================

st.subheader("🤖 AI Positivity Assistant")

user_input = st.text_input(
    "Talk to the AI:"
)

