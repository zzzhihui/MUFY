import streamlit as st
from supabase import create_client
from datetime import date

# -----------------------------
# SUPABASE CONNECT
# -----------------------------
SUPABASE_URL = "YOUR_URL"
SUPABASE_KEY = "YOUR_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# PAGE UI (MOBILE FRIENDLY)
# -----------------------------
st.set_page_config(page_title="Positive App", layout="centered")

st.markdown("""
<style>
.block-container {
    padding: 1.5rem;
    max-width: 600px;
}
input, textarea {
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# LOGIN / REGISTER
# -----------------------------
if st.session_state.user is None:
    st.title("🌸 Positive App")

    mode = st.radio("Choose", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Register":
        if st.button("Create Account"):
            supabase.table("users").insert({
                "username": username,
                "password": password
            }).execute()
            st.success("Account created!")

    if mode == "Login":
        if st.button("Login"):
            res = supabase.table("users")\
                .select("*")\
                .eq("username", username)\
                .eq("password", password)\
                .execute()

            if res.data:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Wrong login")

    st.stop()

# -----------------------------
# LOGGED IN USER
# -----------------------------
user = st.session_state.user
today = str(date.today())

st.title("🌸 Positive Daily App")
st.write(f"👤 Welcome **{user}**")

if st.button("Logout"):
    st.session_state.user = None
    st.rerun()

# -----------------------------
# DAILY QUOTE
# -----------------------------
st.subheader("💬 Daily Quote")

quotes = [
    "You are doing better than you think.",
    "Small progress is still progress.",
    "Rest is productive too.",
    "You are allowed to grow slowly.",
    "Your effort matters."
]

st.success(quotes[hash(today) % len(quotes)])

# -----------------------------
# STREAK SYSTEM
# -----------------------------
streak = supabase.table("streaks")\
    .select("*")\
    .eq("username", user)\
    .execute()

if streak.data:
    data = streak.data[0]
    last_date = data["last_date"]
    current_streak = data["streak"]

    if last_date != today:
        if last_date == str(date.fromordinal(date.today().toordinal() - 1)):
            current_streak += 1
        else:
            current_streak = 1

        supabase.table("streaks").upsert({
            "username": user,
            "last_date": today,
            "streak": current_streak
        }).execute()
else:
    current_streak = 1
    supabase.table("streaks").insert({
        "username": user,
        "last_date": today,
        "streak": current_streak
    }).execute()

st.write(f"🔥 Streak: **{current_streak} days**")

# -----------------------------
# JOURNAL
# -----------------------------
st.subheader("📔 Journal")

entry = st.text_area("Write your thoughts", height=150)

if st.button("Save Journal"):
    supabase.table("journals").insert({
        "username": user,
        "entry": entry,
        "created_at": today
    }).execute()
    st.success("Saved!")

# -----------------------------
# HISTORY
# -----------------------------
if st.checkbox("Show my journals"):
    res = supabase.table("journals")\
        .select("*")\
        .eq("username", user)\
        .order("id", desc=True)\
        .execute()

    for row in res.data:
        st.write("📅", row["created_at"])
        st.write(row["entry"])
        st.write("---")