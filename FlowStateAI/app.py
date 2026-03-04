import streamlit as st
import datetime
import pandas as pd
import random
import plotly.express as px
import time

# Optional AI tutor
try:
    from openai import OpenAI
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Smart Study Companion", page_icon="🧠", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.title{
font-size:42px;
font-weight:bold;
text-align:center;
color:#4CAF50;
}
.card{
background:#1E1E1E;
padding:20px;
border-radius:10px;
margin-bottom:20px;
color:white;
}
.metric-card{
background:#4CAF50;
padding:15px;
border-radius:10px;
text-align:center;
color:white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🧠 AI Smart Study Companion</p>', unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "completed_topics" not in st.session_state:
    st.session_state.completed_topics = 0
if "focus_sessions" not in st.session_state:
    st.session_state.focus_sessions = 0

# ---------- SIDEBAR ----------
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Study Planner", "Focus Timer", "Progress Tracker", "AI Tutor", "Motivation"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.subheader("📊 Productivity Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Focus Score", f"{random.randint(70,95)}%")
    col2.metric("Study Streak", f"{random.randint(3,10)} Days")
    col3.metric("Topics Completed", st.session_state.completed_topics)

    st.divider()
    st.subheader("Weekly Productivity Trend")
    productivity = [random.randint(60,100) for i in range(7)]
    df = pd.DataFrame({"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], "Focus":productivity})
    fig = px.line(df, x="Day", y="Focus", markers=True, title="Weekly Focus Trend")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- STUDY PLANNER ----------------
elif menu == "Study Planner":
    st.subheader("📅 Smart Study Planner")

    exam_date = st.date_input("Select Exam Date")
    hours = st.slider("Study Hours Per Day", 1, 12, 4)
    weak_subject = st.text_input("Enter Your Weak Subject (Optional)")
    topics = st.text_area("Enter Topics (comma separated)")

    if st.button("Generate Plan"):
        today = datetime.date.today()
        days_left = (exam_date - today).days
        topic_list = [t.strip() for t in topics.split(",") if t.strip()]

        if days_left <= 0:
            st.error("❌ Exam date must be in the future")
        elif len(topic_list)==0:
            st.warning("⚠️ Please enter at least one topic")
        else:
            st.success(f"⏳ You have {days_left} days until your exam")
            topics_per_day = max(1, len(topic_list) // days_left)
            st.write(f"💡 Study approximately **{topics_per_day} topics per day**")

            # Dynamic daily plan
            plan = []
            index = 0
            for d in range(days_left):
                today_topics = topic_list[index:index+topics_per_day]
                if weak_subject:
                    # Repeat weak subject topics for extra focus
                    weak_topics_today = [t for t in today_topics if weak_subject.lower() in t.lower()]
                    if not weak_topics_today and weak_subject.lower() in ",".join(topic_list).lower():
                        today_topics.append(weak_subject)
                plan.append({"Day": f"Day {d+1}", "Topics": ", ".join(today_topics)})
                index += topics_per_day

            df_plan = pd.DataFrame(plan)
            st.dataframe(df_plan)

            # Downloadable CSV
            st.download_button(
                "📥 Download Study Plan",
                df_plan.to_csv(index=False),
                file_name="study_plan.csv"
            )

# ---------------- FOCUS TIMER ----------------
elif menu == "Focus Timer":
    st.subheader("⏱ Pomodoro Focus Timer")
    minutes = st.slider("Focus Minutes", 15, 60, 25)
    if st.button("Start Focus Session"):
        total = minutes*60
        timer = st.empty()
        for s in range(total,0,-1):
            mins = s//60
            sec = s%60
            timer.metric("Time Remaining", f"{mins}:{sec:02}")
            time.sleep(1)
        st.success("✅ Focus session finished!")
        st.session_state.focus_sessions += 1

# ---------------- PROGRESS TRACKER ----------------
elif menu == "Progress Tracker":
    st.subheader("📊 Study Progress Tracker")
    total = st.number_input("Total Topics", 1, 500, 50)
    completed = st.slider("Topics Completed", 0, total)
    st.session_state.completed_topics = completed

    progress = completed / total
    st.progress(progress)
    st.write(f"Progress: **{completed}/{total} topics completed**")

    # Gamification badge
    if progress >= 0.8:
        st.balloons()
        st.success("🏆 Study Master Badge Unlocked!")

# ---------------- AI TUTOR ----------------
elif menu == "AI Tutor":
    st.subheader("🤖 AI Study Tutor")
    topic = st.text_input("Ask about a topic")
    api_key = st.text_input("OpenAI API Key (optional)", type="password")
    if st.button("Explain Topic / Generate Quiz"):
        if AI_AVAILABLE and api_key:
            try:
                client = OpenAI(api_key=api_key)
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=f"Explain simply for a student: {topic}\nAlso generate 3 quiz questions for practice."
                )
                st.write(response.output[0].content[0].text)
            except:
                st.error("⚠️ API error or invalid key")
        else:
            st.info("ℹ️ Add OpenAI API key to enable AI tutor")

# ---------------- MOTIVATION ----------------
elif menu == "Motivation":
    st.subheader("💡 Motivation Engine")
    quotes = [
        "Success is the sum of small efforts repeated daily.",
        "Discipline beats motivation.",
        "Consistency creates mastery.",
        "Dream big. Work harder.",
        "Focus like a laser."
    ]
    st.success(random.choice(quotes))
    st.image("https://images.unsplash.com/photo-1506784983877-45594efa4cbe", use_container_width=True)