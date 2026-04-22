import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile

st.title(" Sports Performance Monitoring System")

option = st.selectbox("Choose Option", ["Upload Video", "Live Camera"])

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

speed_data = []


if option == "Upload Video":
    video_file = st.file_uploader("Upload Video", type=["mp4", "mov"])

    if video_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())

        cap = cv2.VideoCapture(tfile.name)
        stframe = st.empty()

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame)

            if results.pose_landmarks:
                mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                speed_data.append(frame_count % 20 + 10)  # dummy speed

            stframe.image(frame)
            frame_count += 1

        cap.release()


elif option == "Live Camera":
    run = st.button("Start Camera")
    stop = st.button("Stop")

    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)

    frame_count = 0

    while run and not stop:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            speed_data.append(frame_count % 20 + 10)  # dummy speed

        FRAME_WINDOW.image(frame)
        frame_count += 1

    cap.release()


if len(speed_data) > 0:
    df = pd.DataFrame({"Frame": list(range(len(speed_data))), "Speed": speed_data})

    st.subheader(" Performance Data")
    st.dataframe(df)

    st.subheader(" Graph")
    fig, ax = plt.subplots()
    ax.plot(df["Frame"], df["Speed"])
    st.pyplot(fig)

    score = int(df["Speed"].mean() * 5)
    st.write(" Score:", score)

    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Sports Performance Report", ln=True)
        pdf.cell(200, 10, txt=f"Score: {score}", ln=True)

        pdf.output("report.pdf")

    if st.button("Generate Report"):
        create_pdf()
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="report.pdf")
import streamlit as st
import cv2

# 🔹 UI SETUP
st.set_page_config(page_title="Sports AI", layout="wide")

st.title("🏋️ Sports Performance Dashboard")
st.subheader("AI Based Live Tracking System")

# 🔹 SIDEBAR
st.sidebar.title("Controls")

exercise = st.sidebar.selectbox("Select Exercise", ["Pushup", "Squat", "Running"])

start = st.sidebar.button("Start")
stop = st.sidebar.button("Stop")

# 🔹 SESSION STATE (IMPORTANT)
if "run" not in st.session_state:
    st.session_state.run = False

if start:
    st.session_state.run = True

if stop:
    st.session_state.run = False

# 🔹 METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Reps", "0")
col2.metric("Accuracy", "0%")
col3.metric("Calories", "0 kcal")

# 🔹 VIDEO SECTION
st.markdown("### 📹 Live Camera")
frame_placeholder = st.empty()

# 🔹 CAMERA LOOP
if st.session_state.run:
    cap = cv2.VideoCapture(0)

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            break

        frame_placeholder.image(frame, channels="BGR")

        # stop button check (important for Streamlit)
        if not st.session_state.run:
            break

    cap.release()
    cv2.destroyAllWindows()

# 🔹 STYLE
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
h1, h2, h3 {
    color: #22c55e;
}
</style>
""", unsafe_allow_html=True)
