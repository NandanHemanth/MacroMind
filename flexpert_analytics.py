import streamlit as st
import json
import sqlite3
import pandas as pd
import plotly.express as px
import datetime
import requests
import os
from dotenv import load_dotenv

# Load API key for Gemini AI
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# File paths
EXERCISE_LOG_PATH = "./database/exercise_log.json"
USER_DATA_PATH = "./database/user_data.json"
MEAL_PLAN_LOG_PATH = "./database/meal_plan_log.json"
DB_PATH = "./database/user_exercises.db"

def load_json_data(file_path):
    """Loads JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_meal_plan_log(meal_plan, fitness_goal):
    """Logs generated meal plans into a JSON file."""
    new_entry = {
        "date": str(datetime.date.today()),
        "fitness_goal": fitness_goal,
        "meal_plan": meal_plan
    }
    existing_data = load_json_data(MEAL_PLAN_LOG_PATH)
    existing_data.append(new_entry)
    with open(MEAL_PLAN_LOG_PATH, "w") as file:
        json.dump(existing_data, file, indent=4)

def load_sqlite_data():
    """Loads user exercise data from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM exercise_log", conn)
    conn.close()
    return df

def fetch_meal_plan(detected_foods, fitness_goal):
    """Generates a customized meal plan based on user fitness goals."""
    query = f"Generate a meal plan for a person focusing on {fitness_goal} with these ingredients: {', '.join(detected_foods)}."
    data = {"contents": [{"parts": [{"text": query}]}]}
    response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=data)
    if response.status_code == 200:
        meal_plan = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        save_meal_plan_log(meal_plan, fitness_goal)
        return meal_plan
    return "❌ Error generating meal plan."

# Load data
exercise_log = load_json_data(EXERCISE_LOG_PATH)
user_data = load_json_data(USER_DATA_PATH)
exercise_df = load_sqlite_data()

# Extract user details
fitness_goal = user_data.get("goal", "Maintain")
detected_foods = [log.get("exercise_name", "Unknown") for log in exercise_log]

# Generate meal plan using AI
meal_plan = fetch_meal_plan(detected_foods, fitness_goal)

# Streamlit UI
st.header("📊 Your Fitness Journey with Flexpert")
st.write("Track your **progress** and stay motivated! 📈")

# Display meal plan
st.subheader("🍽 Customized Meal Plan")
st.write(meal_plan)

# Display analytics charts
st.subheader("📊 Workout Performance")
fig = px.bar(exercise_df, x="exercise_name", y="calories", color="exercise_name", title="Calories Burned by Exercise")
st.plotly_chart(fig)

fig2 = px.line(exercise_df, x="exercise_name", y="score", color="exercise_name", title="Workout Form Scores Over Time")
st.plotly_chart(fig2)

st.sidebar.info("💡 Stay consistent! Track your workouts and diet to maximize results.")
