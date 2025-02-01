import mediapipe as mp
import cv2
import numpy as np
import math
import time
import streamlit as st

# Initialize Pose Model
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Define Workouts
WORKOUTS = {
    "Bicep Curls": (11, 13, 15),  # Shoulder, Elbow, Wrist
    "Squats": (24, 26, 28),       # Hip, Knee, Ankle
    "Push-ups": (12, 14, 16)      # Shoulder, Elbow, Wrist
}

WORKOUT_FLOW = ["Bicep Curls", "Squats", "Push-ups"]
current_workout_index = 0
reps_completed = 0

# Streamlit UI
st.title("Smart Workout Tracker 🏋️‍♂️")
selected_workout = st.selectbox("Choose a workout:", list(WORKOUTS.keys()))

if st.button("Start Workout"):
    st.write(f"Starting {selected_workout}... Keep moving!")

    cap = cv2.VideoCapture(0)
    pTime = 0
    dir = 0
    count = 0

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        lmList = []

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            if len(lmList) != 0:
                # Get the selected workout landmarks
                p1, p2, p3 = WORKOUTS[selected_workout]

                # Calculate angle
                x1, y1 = lmList[p1][1:]
                x2, y2 = lmList[p2][1:]
                x3, y3 = lmList[p3][1:]

                angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
                if angle < 0:
                    angle += 360

                # Map angle to percentage
                per = np.interp(angle, (60, 160), (100, 0))

                if per == 100 and dir == 0:
                    count += 0.5
                    reps_completed += 0.5
                    dir = 1

                if per == 0 and dir == 1:
                    count += 0.5
                    reps_completed += 0.5
                    dir = 0

                # Display count
                cv2.putText(img, str(count), (500, 75), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        # FPS Calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Check if reps completed and move to next workout
    if reps_completed >= 10:
        next_workout_name = next_workout()
        if next_workout_name:
            st.write(f"Next Workout: {next_workout_name} 💪")
        else:
            st.write("Workout session complete! 🎉")

