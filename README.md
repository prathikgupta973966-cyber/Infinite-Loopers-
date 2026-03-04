import streamlit as st
import pandas as pd
import sqlite3
import datetime
import plotly.express as px
import random
import time

st.set_page_config(page_title="SmartStudy OS", layout="wide")

# ---------------- DATABASE ----------------

# DATABASE
conn = sqlite3.connect("study.db", check_same_thread=False)
cursor = conn.cursor()

# LOGIN SYSTEM
if "user" not in st.session_state:
    st.session_state.user = None

# 👉 ADD THIS PART HERE
df = pd.read_sql_query(
    "SELECT * FROM records WHERE username=?",
    conn,
    params=(st.session_state.user,)
)

# SIDEBAR
with st.sidebar:
    ...
# ---------------- STYLE ----------------

# ---------------- PREMIUM STYLE ----------------

st.markdown("""
<style>

/* FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

/* SIDEBAR STYLE */
[data-testid="stSidebar"]{
background: linear-gradient(180deg,#141E30,#243B55);
border-right:1px solid rgba(255,255,255,0.1);
}

/* TITLE */
.title{
font-size:60px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#00DBDE,#FC00FF);
-webkit-background-clip:text;
color:transparent;
margin-bottom:20px;
}

/* SUBTITLE */
.subtitle{
text-align:center;
color:#cccccc;
margin-bottom:30px;
}

/* METRIC CARDS */
[data-testid="metric-container"]{
background: rgba(255,255,255,0.08);
padding:15px;
border-radius:15px;
box-shadow:0 6px 20px rgba(0,0,0,0.4);
}

/* BUTTON STYLE */
.stButton>button{
background: linear-gradient(90deg,#00DBDE,#FC00FF);
color:white;
border:none;
border-radius:12px;
padding:10px 25px;
font-weight:600;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.05);
box-shadow:0 4px 15px rgba(0,0,0,0.5);
}

/* INPUT BOXES */
input, textarea{
border-radius:10px !important;
}

/* DATAFRAME STYLE */
[data-testid="stDataFrame"]{
background: rgba(255,255,255,0.05);
border-radius:10px;
padding:10px;
}

/* PROGRESS BAR */
.stProgress > div > div > div > div{
background: linear-gradient(90deg,#00DBDE,#FC00FF);
}

/* CARD DESIGN */
.card{
background: rgba(255,255,255,0.08);
padding:20px;
border-radius:15px;
backdrop-filter: blur(10px);
box-shadow:0px 6px 20px rgba(0,0,0,0.3);
margin-bottom:20px;
}

/* CARD HOVER */
.card:hover{
transform: translateY(-4px);
box-shadow:0px 10px 30px rgba(0,0,0,0.5);
transition:0.3s;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SYSTEM ----------------

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.subheader("Login / Register")

    choice = st.radio("Select",["Login","Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":

        if st.button("Create Account"):

            cursor.execute("INSERT INTO users VALUES (?,?)",(username,password))
            conn.commit()

            st.success("Account created. Please login.")

    if choice == "Login":

        if st.button("Login"):

            cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
            data = cursor.fetchone()

            if data:
                st.session_state.user = username
                st.success("Login successful")
            else:
                st.error("Invalid credentials")

    st.stop()

# ---------------- SIDEBAR ----------------

# ---------------- PREMIUM STYLE ----------------

st.markdown("""
<style>

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"]{
background: linear-gradient(180deg,#141E30,#243B55);
padding-top:20px;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] *{
color:white;
}

/* TITLE STYLE */
.title{
font-size:55px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#00DBDE,#FC00FF);
-webkit-background-clip:text;
color:transparent;
margin-bottom:20px;
}

/* BUTTON STYLE */
.stButton>button{
background: linear-gradient(90deg,#00DBDE,#FC00FF);
color:white;
border:none;
border-radius:10px;
padding:8px 20px;
font-weight:600;
}

/* METRIC CARDS */
[data-testid="metric-container"]{
background: rgba(255,255,255,0.08);
border-radius:12px;
padding:10px;
}

/* USER CARD */
.user-card{
background: rgba(255,255,255,0.1);
padding:15px;
border-radius:12px;
text-align:center;
margin-bottom:15px;
font-size:16px;
}

/* DATAFRAME STYLE */
[data-testid="stDataFrame"]{
background: rgba(255,255,255,0.05);
border-radius:10px;
padding:10px;
}

/* PROGRESS BAR */
.stProgress > div > div > div > div{
background: linear-gradient(90deg,#00DBDE,#FC00FF);
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

# ---------------- APP TITLE ----------------

st.markdown("""
<h1 style='
text-align:center;
font-size:60px;
font-weight:800;
background: linear-gradient(90deg,#00DBDE,#FC00FF);
-webkit-background-clip:text;
color:transparent;
margin-bottom:10px;
'>
🚀 SmartStudy OS
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='
text-align:center;
font-size:20px;
color:#dcdcdc;
margin-bottom:40px;
'>
AI Powered Smart Study Companion
</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("### 📚 SmartStudy Menu")

    if "user" in st.session_state:
        st.markdown(f"""
        <div class="user-card">
        👤 <b>{st.session_state.user}</b>
        </div>
        """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        [
        "Dashboard",
        "Exam Planner",
        "Study Planner",
        "Progress Tracker",
        "Analytics",
        "Weak Topic Detection",
        "AI Study Recommendation",
        "Study Heatmap",
        "Pomodoro Timer",
        "Achievements",
        "Motivation",
        "Topper Study Guide",
        "Final Report"
        ]
    )

    st.divider()
    st.caption("SmartStudy OS v1.0")
# ---------------- LOAD USER DATA ----------------

# ---------------- LOGIN SYSTEM ----------------

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.subheader("🔐 Login / Register")

    choice = st.radio("Select Option", ["Login","Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":

        if st.button("Create Account"):

            try:

                cursor.execute(
                "INSERT INTO users (username,password) VALUES (?,?)",
                (username,password)
                )

                conn.commit()

                st.success("Account created successfully!")

            except:

                st.error("Username already exists")

    if choice == "Login":

        if st.button("Login"):

            cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
            )

            data = cursor.fetchone()

            if data:

                st.session_state.user = username

                st.success("Login successful")

                st.rerun()

            else:

                st.error("Invalid username or password")

    st.stop()

# ================= DASHBOARD =================

# ================= DASHBOARD =================

# ================= DASHBOARD =================

if menu == "Dashboard":

    st.subheader("📊 Smart Study Dashboard")

    if not df.empty:

        total_hours = df["hours"].sum()
        total_topics = df["topic"].nunique()
        subjects = df["subject"].nunique()

        col1,col2,col3 = st.columns(3)

        col1.metric("📚 Topics Studied", total_topics)
        col2.metric("⏱ Study Hours", total_hours)
        col3.metric("📊 Subjects Covered", subjects)

        st.divider()

        tab1,tab2,tab3 = st.tabs(
        ["📊 Subject Analysis","📈 Study Trend","🔥 Top Topics"]
        )

        # SUBJECT ANALYSIS
        with tab1:

            subject_hours = df.groupby("subject")["hours"].sum().reset_index()

            fig = px.bar(
                subject_hours,
                x="subject",
                y="hours",
                color="subject",
                title="Study Hours per Subject"
            )

            st.plotly_chart(fig,use_container_width=True)

        # DAILY STUDY TREND
        with tab2:

            df["date"] = pd.to_datetime(df["date"])

            daily = df.groupby("date")["hours"].sum().reset_index()

            fig2 = px.line(
                daily,
                x="date",
                y="hours",
                markers=True,
                title="Daily Study Progress"
            )

            st.plotly_chart(fig2,use_container_width=True)

        # TOP TOPICS
        with tab3:

            top_topics = df.groupby("topic")["hours"].sum().sort_values(
            ascending=False).head(5)

            fig3 = px.bar(
                top_topics.reset_index(),
                x="topic",
                y="hours",
                color="hours",
                title="Most Studied Topics"
            )

            st.plotly_chart(fig3,use_container_width=True)

        st.divider()

        st.subheader("📈 Study Progress")

        target_hours = 100

        progress = min(1,total_hours/target_hours)

        st.progress(progress)

        st.write(f"{round(progress*100)}% of study target completed")

        st.divider()

        st.subheader("🧠 Performance Insight")

        subject_analysis = df.groupby("subject")["hours"].sum()

        strong = subject_analysis.idxmax()
        weak = subject_analysis.idxmin()

        col4,col5 = st.columns(2)

        col4.success(f"Strong Subject: {strong}")
        col5.error(f"Needs More Focus: {weak}")

    else:

        st.info("Start adding study sessions to see your dashboard analytics.")

# ================= STUDY PLANNER =================

elif menu == "Study Planner":

    subject = st.selectbox(
    "Subject",
    ["Math","Physics","Chemistry","Programming","Electronics"]
    )

    topics = {

    "Math":[
    "Algebra","Calculus","Matrices","Differential Equations","Probability"],

    "Physics":[
    "Kinematics","Laws of Motion","Work Energy Power","Electrostatics","Magnetism"],

    "Chemistry":[
    "Atomic Structure","Chemical Bonding","Thermodynamics","Organic Chemistry","Electrochemistry"],

    "Programming":[
    "Variables","Loops","Functions","Data Structures","Algorithms"],

    "Electronics":[
    "Logic Gates","Boolean Algebra","Adders","Flip Flops","Registers"]

    }

    topic = st.selectbox("Topic",topics[subject])

    hours = st.slider("Study Hours",1,8)

    difficulty = st.selectbox("Difficulty",["Easy","Medium","Hard"])

    if st.button("Save Session"):

        cursor.execute(
        "INSERT INTO records VALUES (?,?,?,?,?,?)",
        (st.session_state.user,subject,topic,hours,difficulty,str(datetime.date.today()))
        )

        conn.commit()

        st.success("Study session saved")

# ================= PROGRESS =================

# ================= PROGRESS TRACKER =================

elif menu == "Progress Tracker":

    st.subheader("📈 Study Progress Tracker")

    if not df.empty:

        total_topics = len(df)
        completed_topics = df["topic"].nunique()

        progress = completed_topics / total_topics

        st.progress(progress)

        col1,col2 = st.columns(2)

        col1.metric("Total Study Sessions", total_topics)
        col2.metric("Unique Topics Studied", completed_topics)

        st.divider()

        st.subheader("📚 Subject Progress")

        subject_hours = df.groupby("subject")["hours"].sum()

        for subject,hours in subject_hours.items():

            progress_value = min(hours / 20, 1)

            st.write(subject)

            st.progress(progress_value)

        st.divider()

        st.subheader("📊 Progress Distribution")

        progress_data = df.groupby("subject")["hours"].sum().reset_index()

        fig = px.bar(
            progress_data,
            x="subject",
            y="hours",
            color="subject",
            title="Study Progress by Subject"
        )

        st.plotly_chart(fig,use_container_width=True)

        st.divider()

        st.subheader("🏁 Study Milestones")

        total_hours = df["hours"].sum()

        if total_hours >= 5:
            st.success("✔ First 5 Study Hours Completed")

        if total_hours >= 20:
            st.success("✔ 20 Study Hours Milestone")

        if total_hours >= 50:
            st.success("✔ 50 Study Hours Milestone")

    else:

        st.warning("Add study sessions to track progress.")

# ================= ANALYTICS =================

# ================= ANALYTICS =================

elif menu == "Analytics":

    st.subheader("📊 Study Analytics Dashboard")

    if not df.empty:

        df["date"] = pd.to_datetime(df["date"])

        col1,col2 = st.columns(2)

        with col1:

            st.subheader("📚 Study Hours by Subject")

            subject_hours = df.groupby("subject")["hours"].sum().reset_index()

            fig = px.bar(
                subject_hours,
                x="subject",
                y="hours",
                color="subject",
                title="Study Time Distribution"
            )

            st.plotly_chart(fig,use_container_width=True)

        with col2:

            st.subheader("📈 Daily Study Trend")

            daily_hours = df.groupby("date")["hours"].sum().reset_index()

            fig2 = px.line(
                daily_hours,
                x="date",
                y="hours",
                markers=True,
                title="Daily Study Hours"
            )

            st.plotly_chart(fig2,use_container_width=True)

        st.divider()

        col3,col4 = st.columns(2)

        with col3:

            st.subheader("📊 Difficulty Distribution")

            difficulty_data = df.groupby("difficulty").size().reset_index(name="count")

            fig3 = px.pie(
                difficulty_data,
                values="count",
                names="difficulty",
                title="Study Difficulty Levels"
            )

            st.plotly_chart(fig3,use_container_width=True)

        with col4:

            st.subheader("🔥 Most Studied Topics")

            topic_hours = df.groupby("topic")["hours"].sum().sort_values(ascending=False).head(5)

            topic_df = topic_hours.reset_index()

            fig4 = px.bar(
                topic_df,
                x="topic",
                y="hours",
                color="hours",
                title="Top Topics"
            )

            st.plotly_chart(fig4,use_container_width=True)

        st.divider()

        st.subheader("📅 Study Consistency")

        study_days = df["date"].nunique()
        total_hours = df["hours"].sum()

        col5,col6 = st.columns(2)

        col5.metric("Study Days", study_days)
        col6.metric("Total Study Hours", total_hours)

        if study_days >= 5:
            st.success("🔥 Good consistency in studying!")

        else:
            st.warning("Try studying more regularly.")

    else:

        st.warning("Add study sessions to see analytics.")

# ================= WEAK TOPIC DETECTION =================

# ================= WEAK TOPIC DETECTION =================

elif menu == "Weak Topic Detection":

    st.subheader("⚠ Weak Topic Detection")

    if not df.empty:

        topic_hours = df.groupby("topic")["hours"].sum().sort_values()

        weak_topics = topic_hours.head(5)

        st.error("Topics needing more practice")

        for topic,hrs in weak_topics.items():

            st.write(f"🔴 {topic}  → studied only {hrs} hours")

        st.divider()

        st.subheader("📚 Recommended Practice Time")

        recommendations = []

        for topic,hrs in weak_topics.items():

            if hrs < 2:
                recommendations.append((topic,"Practice 2–3 hours"))
            elif hrs < 5:
                recommendations.append((topic,"Practice 1–2 hours"))
            else:
                recommendations.append((topic,"Quick revision"))

        rec_df = pd.DataFrame(
            recommendations,
            columns=["Topic","Recommended Practice"]
        )

        st.table(rec_df)

        st.divider()

        st.subheader("🎯 Priority Topics")

        priority = list(weak_topics.index)

        for i,topic in enumerate(priority):

            st.write(f"{i+1}. {topic}")

        st.info("Start practicing topics in this order.")

    else:

        st.warning("Add study sessions to detect weak topics.")

# ================= AI STUDY RECOMMENDATION =================

# ================= AI STUDY RECOMMENDATION =================

elif menu == "AI Study Recommendation":

    st.subheader("🧠 AI Study Recommendation System")

    if not df.empty:

        subject_hours = df.groupby("subject")["hours"].sum().sort_values()

        weak_subject = subject_hours.idxmin()
        strong_subject = subject_hours.idxmax()

        st.error(f"⚠ Weak Subject: {weak_subject}")
        st.success(f"💪 Strong Subject: {strong_subject}")

        st.divider()

        st.subheader("📊 Subject Priority Order")

        priority = subject_hours.sort_values()

        for i,sub in enumerate(priority.index):

            st.write(f"{i+1}. {sub}")

        st.divider()

        st.subheader("📚 Weak Topics Needing Practice")

        topic_hours = df.groupby("topic")["hours"].sum().sort_values()

        weak_topics = topic_hours.head(3)

        for t in weak_topics.index:

            st.warning(f"Practice Topic: {t}")

        st.divider()

        st.subheader("⏱ Recommended Study Hours")

        recommendation = {}

        for sub in subject_hours.index:

            hrs = subject_hours[sub]

            if hrs < 5:
                recommendation[sub] = "3 hours/day"
            elif hrs < 10:
                recommendation[sub] = "2 hours/day"
            else:
                recommendation[sub] = "1 hour/day revision"

        rec_df = pd.DataFrame(
            list(recommendation.items()),
            columns=["Subject","Recommended Hours"]
        )

        st.table(rec_df)

        st.divider()

        st.subheader("📅 Suggested Study Plan for Today")

        weak = subject_hours.index[0]
        second = subject_hours.index[1] if len(subject_hours) > 1 else weak

        st.success(f"""
        1️⃣ Study **{weak}** for 2 hours  
        2️⃣ Practice weak topics in **{weak}**  
        3️⃣ Study **{second}** for 1 hour  
        4️⃣ Revise strongest subject for 30 minutes  
        """)

    else:

        st.warning("Add study sessions first to generate recommendations.")

# ================= STUDY HEATMAP =================

# ================= STUDY HEATMAP =================

elif menu == "Study Heatmap":

    st.subheader("📅 Study Activity Heatmap")

    if not df.empty:

        df["date"] = pd.to_datetime(df["date"])

        # Sum hours per day
        daily = df.groupby("date")["hours"].sum().reset_index()

        daily["day"] = daily["date"].dt.day
        daily["month"] = daily["date"].dt.month
        daily["year"] = daily["date"].dt.year

        fig = px.scatter(
            daily,
            x="date",
            y="hours",
            size="hours",
            color="hours",
            color_continuous_scale="Turbo",
            title="Daily Study Intensity"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info("Larger & darker circles = More study hours")

        st.divider()

        st.subheader("📊 Weekly Study Pattern")

        daily["weekday"] = daily["date"].dt.day_name()

        weekly = daily.groupby("weekday")["hours"].sum().reset_index()

        fig2 = px.bar(
            weekly,
            x="weekday",
            y="hours",
            color="hours",
            color_continuous_scale="Blues"
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:

        st.warning("No study data available yet.")

# ================= POMODORO TIMER =================

# ================= POMODORO TIMER =================

elif menu == "Pomodoro Timer":

    st.subheader("⏱ Pomodoro Focus Timer")

    if "sessions" not in st.session_state:
        st.session_state.sessions = 0

    work_minutes = st.slider("Focus Time (minutes)",15,60,25)
    break_minutes = st.slider("Break Time (minutes)",5,20,5)

    col1,col2 = st.columns(2)

    with col1:
        start = st.button("▶ Start Focus Session")

    with col2:
        reset = st.button("🔄 Reset Timer")

    if reset:
        st.session_state.sessions = 0
        st.success("Timer reset")

    if start:

        total = work_minutes * 60

        progress = st.progress(0)
        timer_display = st.empty()

        for i in range(total):

            remaining = total - i

            minutes = remaining // 60
            seconds = remaining % 60

            timer_display.metric("Focus Time Remaining", f"{minutes}:{seconds:02}")

            progress.progress(i / total)

            time.sleep(1)

        st.success("🎉 Focus session complete!")

        st.session_state.sessions += 1

        st.subheader("🌿 Break Time")

        break_total = break_minutes * 60

        break_progress = st.progress(0)
        break_timer = st.empty()

        for i in range(break_total):

            remaining = break_total - i

            minutes = remaining // 60
            seconds = remaining % 60

            break_timer.metric("Break Remaining", f"{minutes}:{seconds:02}")

            break_progress.progress(i / break_total)

            time.sleep(1)

        st.info("Break finished. Ready for next session!")

    st.divider()

    st.subheader("📊 Pomodoro Stats")

    st.metric("Focus Sessions Completed", st.session_state.sessions)

    if st.session_state.sessions >= 4:
        st.success("🔥 Great productivity today!")

# ================= ACHIEVEMENTS =================

# ================= ACHIEVEMENTS =================

elif menu == "Achievements":

    st.subheader("🏆 Achievements & Study Insights")

    if not df.empty:

        total_hours = df["hours"].sum()
        total_topics = len(df)

        col1,col2 = st.columns(2)

        col1.metric("Total Topics Studied", total_topics)
        col2.metric("Total Study Hours", total_hours)

        st.divider()

        st.subheader("🎖 Achievements")

        if total_hours >= 5:
            st.success("🔥 First 5 Hours Studied")

        if total_hours >= 20:
            st.success("⚡ 20 Hour Focus Master")

        if total_topics >= 10:
            st.success("📚 10 Topics Completed")

        if total_hours >= 50:
            st.success("🚀 Study Champion")

        st.divider()

        st.subheader("📊 Subject Study Analysis")

        subject_hours = df.groupby("subject")["hours"].sum().sort_values(ascending=False)

        st.dataframe(subject_hours)

        st.subheader("🎯 Study Priority Recommendation")

        strong = subject_hours.idxmax()
        weak = subject_hours.idxmin()

        st.success(f"Strong Subject: {strong}")
        st.error(f"Needs More Focus: {weak}")

        st.info("Priority Order (Study first → last):")

        priority = subject_hours.sort_values()

        for i,sub in enumerate(priority.index):

            st.write(f"{i+1}. {sub}")

        st.divider()

        st.subheader("⏱ Recommended Study Hours")

        recommended = {}

        for sub in subject_hours.index:

            hrs = subject_hours[sub]

            if hrs < 5:
                recommended[sub] = "3 hours/day"
            elif hrs < 10:
                recommended[sub] = "2 hours/day"
            else:
                recommended[sub] = "1 hour/day (revision)"

        rec_df = pd.DataFrame(list(recommended.items()),columns=["Subject","Recommended Study Time"])

        st.table(rec_df)

    else:

        st.warning("No study data available yet.")

# ================= MOTIVATION =================
# ================= MOTIVATION =================

elif menu == "Motivation":

    st.subheader("💡 Daily Motivation")

    quotes = [

    "Success is built on daily discipline.",
    "Consistency beats motivation.",
    "Small progress every day leads to big results.",
    "Focus on learning, not just finishing.",
    "Your future self will thank you.",
    "Top students are made by habits, not talent.",
    "Progress is better than perfection.",
    "Hard work compounds like interest."

    ]

    st.success(random.choice(quotes))

    st.divider()

    st.subheader("🎯 Study Reminder")

    reminders = [

    "Plan what you will study before opening books.",
    "Solve problems, don't just read theory.",
    "Revise yesterday's topic for 10 minutes.",
    "Remove distractions before starting study.",
    "Write notes while learning.",
    "Test yourself after finishing a topic."

    ]

    st.info(random.choice(reminders))

    st.divider()

    st.subheader("🔥 Productivity Tips")

    tips = [

    "Study in 40–50 minute focus blocks.",
    "Keep phone away while studying.",
    "Explain concepts as if teaching someone.",
    "Practice weak topics first.",
    "Review mistakes regularly.",
    "Sleep well to improve memory."

    ]

    for tip in tips:

        st.write("✔", tip)

    st.divider()

    st.subheader("⭐ Daily Affirmation")

    affirmations = [

    "I am improving every day.",
    "My effort today builds my future.",
    "I can master difficult concepts.",
    "Consistency will make me successful.",
    "Every study session makes me stronger."

    ]

    st.warning(random.choice(affirmations))

# ================= TOPPER STUDY GUIDE =================

elif menu == "Topper Study Guide":

    st.subheader("🧠 Topper Study System")

    st.markdown("""
**Clear Study System**  
Plan daily topics, problems, and revision.

**Deep Work Blocks**  
50 min study + 10 min break.

**Write While Studying**  
Write formulas, diagrams, and notes.

**Active Recall**  
Explain concepts without looking.

**Daily Revision**  
10 min next day, 20 min weekly.

**Practice Problems**  
Understanding comes from solving.

**One Rough Notebook**  
Track mistakes and formulas.

**Small Daily Targets**  
1 concept + 10 problems + revision.

**Control Distractions**  
Phone away, clean desk.

**Teach Yourself**  
Explain topics like a teacher.

**Concept First**  
Understand before memorizing.

**Proper Rest**  
Sleep 7–8 hours.

**Consistency**  
Study daily, not randomly.
""")

# ================= FINAL REPORT =================

# ================= EXAM PLANNER =================

elif menu == "Exam Planner":

    st.subheader("📅 Smart Exam Planner")

    exam_date = st.date_input("Select Exam Date")

    total_topics = st.number_input("Total Topics to Complete",1,500,50)

    hours_per_topic = st.slider("Average Hours per Topic",1,5,2)

    today = datetime.date.today()

    if exam_date > today:

        days_left = (exam_date - today).days

        total_hours_needed = total_topics * hours_per_topic

        daily_hours = round(total_hours_needed / days_left,2)

        topics_per_day = round(total_topics / days_left,2)

        st.divider()

        col1,col2,col3 = st.columns(3)

        col1.metric("Days Remaining", days_left)
        col2.metric("Total Study Hours Needed", total_hours_needed)
        col3.metric("Daily Study Hours", daily_hours)

        st.divider()

        st.subheader("📚 Daily Study Plan")

        st.write(f"Study **{topics_per_day} topics per day**")

        st.write(f"Study **{daily_hours} hours per day**")

        st.divider()

        progress = min(1,(len(df)/total_topics))

        st.subheader("📈 Syllabus Progress")

        st.progress(progress)

        st.write(f"{len(df)} / {total_topics} topics studied")

        st.divider()

        st.subheader("🎯 Study Priority")

        if not df.empty:

            subject_hours = df.groupby("subject")["hours"].sum()

            weak = subject_hours.idxmin()

            strong = subject_hours.idxmax()

            st.error(f"Focus More On: {weak}")

            st.success(f"Strong Subject: {strong}")

        else:

            st.info("Add study sessions to get priority analysis")

    else:

        st.error("Exam date must be in the future")
