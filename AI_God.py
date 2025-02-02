import mediapipe as mp
import cv2
import numpy as np
import math
import time
import sys
import sqlite3
import matplotlib.pyplot as plt
import json

# Get exercise and rep count from command-line arguments
if len(sys.argv) < 3:
    print("Error: Please provide an exercise name and rep count.")
    sys.exit(1)

exercise_name = sys.argv[1]
rep_count = int(sys.argv[2])

# Database Setup
def init_db():
    conn = sqlite3.connect("./database/user_exercises.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS exercise_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        exercise_id INTEGER,
                        exercise_name TEXT,
                        reps INTEGER,
                        score REAL,
                        calories REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_exercise(exercise_id, exercise_name, reps, score, calories):
    conn = sqlite3.connect("./database/user_exercises.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exercise_log (exercise_id, exercise_name, reps, score, calories) VALUES (?, ?, ?, ?, ?)", 
                   (exercise_id, exercise_name, reps, score, calories))
    conn.commit()
    conn.close()

init_db()

def findAngle(img, lmList, p1, p2, p3, draw=True):
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]
    
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    
    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
        cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    return angle

# Define exercise landmark mappings and calorie burn per rep
WORKOUTS = {
    "Bicep Curls": (11, 13, 15),  # Shoulder, Elbow, Wrist
    "Squats": (24, 26, 28),       # Hip, Knee, Ankle
    "Push-ups": (12, 14, 16),     # Shoulder, Elbow, Wrist
    "Lunges": (24, 26, 28),       # Hip, Knee, Ankle
    "Deadlifts": (24, 26, 28),    # Hip, Knee, Ankle
    "Planks": (12, 14, 16),       # Shoulder, Elbow, Wrist
    "Bench Press": (12, 14, 16)   # Shoulder, Elbow, Wrist
}

CALORIES_PER_REP = {
    "Bicep Curls": 0.5,
    "Squats": 0.8,
    "Push-ups": 0.7,
    "Lunges": 0.6,
    "Deadlifts": 1.2,
    "Planks": 0.3,
    "Bench Press": 1.0
}

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

pTime = 0
dir = 0
count = 0
cap = cv2.VideoCapture(0)

# Timer for exercise duration
exercise_duration = rep_count * 8  # Each rep is 10 seconds
start_time = time.time()
end_time = time.time() + exercise_duration
score_list = []

print(time.time())
print(start_time)
print(end_time)

while (time.time() - end_time) < 0:
    success, img = cap.read()
    if not success:
        break
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    
    lmList = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])

        if len(lmList) != 0 and exercise_name in WORKOUTS:
            p1, p2, p3 = WORKOUTS[exercise_name]
            angle = findAngle(img, lmList, p1, p2, p3)
            per = np.interp(angle, (60, 160), (100, 0))
            score_list.append(per)
            
            if per == 100 and dir == 0:
                count += 0.5
                dir = 1
            if per == 0 and dir == 1:
                count += 0.5
                dir = 0
            
            cv2.putText(img, str(count), (500, 75), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(img, "Time Left: " + str(int(end_time - time.time())), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    cv2.imshow("Workout Tracker", img)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# Compute final score and calories burned
average_score = sum(score_list) / len(score_list) if score_list else 0
calories_burned = CALORIES_PER_REP.get(exercise_name, 0) * int(count)
log_exercise(100, exercise_name, int(count), average_score, calories_burned)

# Save score chart for Streamlit
plt.plot(score_list, label="Form Score")
plt.axhline(y=100, color='r', linestyle='--', label="CBum's Form")
plt.xlabel("Frames")
plt.ylabel("Score (%)")
plt.title(f"{exercise_name} Form Score Comparison")
plt.legend()
plt.savefig("./database/form_score_chart.png")  # Save chart for Streamlit display

print(f"Workout {exercise_name} completed with {int(count)} reps! Score: {average_score:.2f}% | Calories Burned: {calories_burned:.2f}")
print("./database/form_score_chart.png")  # Print chart path for Streamlit to read
