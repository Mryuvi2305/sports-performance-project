import cv2
import mediapipe as mp
from utils import calculate_angle
from report import generate_report

def run_video():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture("video.mp4")
    
    counter = 0
    stage = None

    angles = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640,480))

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[11].x, landmarks[11].y]
            elbow = [landmarks[13].x, landmarks[13].y]
            wrist = [landmarks[15].x, landmarks[15].y]

            angle = calculate_angle(shoulder, elbow, wrist)
            angles.append(angle)

            if angle > 160:
                stage = "down"
            if angle < 40 and stage == "down":
                stage = "up"
                counter += 1

            cv2.putText(image, f"Reps: {counter}", (10,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        except:
            pass

        cv2.imshow("Video", image)

        if cv2.waitKey(10) & 0xFF == 27:
          break

    cap.release()
    cv2.destroyAllWindows()

    
    generate_report(counter, angles)