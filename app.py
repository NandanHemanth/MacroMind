import streamlit as st
import requests
import json
import os
import subprocess
import sqlite3
from streamlit_lottie import st_lottie
from PIL import Image
from keto_god import recognize_food, get_nutrition_facts, suggest_recipes
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="MacroMind", page_icon="💪", layout="wide")

# Database setup
DB_PATH = "./database/user_data.db"

def init_db():
    if not os.path.exists("./database"):
        os.makedirs("./database")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        height INTEGER,
                        weight INTEGER,
                        goal TEXT,
                        dietary_restriction TEXT)''')
    conn.commit()
    conn.close()

def save_user_data(name, height, weight, goal, dietary_restriction):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO user_profile (id, name, height, weight, goal, dietary_restriction) 
                      VALUES (1, ?, ?, ?, ?, ?)''', (name, height, weight, goal, dietary_restriction))
    conn.commit()
    conn.close()

def load_user_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, height, weight, goal, dietary_restriction FROM user_profile WHERE id=1")
    data = cursor.fetchone()
    conn.close()
    return data if data else ("", 170, 70, "", "")

# Initialize Database
init_db()

# Function to load Lottie animations from a URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations from URLs
keto_kat_animation = load_lottie_url('https://lottie.host/89ed7481-222e-4850-879d-a96471c32534/3hVtb56VQF.json')  # Cat with food
cbuminator_animation = load_lottie_url('https://lottie.host/0aa94491-176f-4cfd-a7a3-48fdc2cbc844/A3C89do9KL.json')  # Workout theme
pet_animation = load_lottie_url("https://lottie.host/27b7d9f3-211d-4ce8-b8a3-453d3e2c5439/0YWqdBtdv7.json") # Pet doggo

# Sidebar Navigation
st.sidebar.title("🚀 MacroMind Menu")
page = st.sidebar.radio("Personal AI Hub", ["🏠 Profile", "🏋️ Cbuminator", "🥗 Keto-Kat", "📊 Flexpert"])

# Add a space before pet animation for better positioning
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
with st.sidebar:
    st_lottie(pet_animation, height=150, key="keto_pet")


# Profile Section
if page == "🏠 Profile":
    st.header("🏠 Your Profile")
    st.write("Enter your details to personalize your fitness journey.")
    
    # Display Profile Picture
    st.markdown("""
        <style>
        .profile-pic {
            display: flex;
            justify-content: center;
        }
        img {
            border-radius: 50%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("./assets/keto_kat.webp", width=150)
    
    # Load existing data
    name, height, weight, goal, dietary_restriction = load_user_data()
    
    name = st.text_input("👤 Name:", name)
    height = st.number_input("📏 Height (cm):", min_value=100, max_value=250, value=height)
    weight = st.number_input("⚖️ Weight (kg):", min_value=30, max_value=200, value=weight)
    
    # Fitness goals dropdown
    goals = {
        "Bulking": "Increase muscle mass with a calorie surplus.",
        "Cutting": "Reduce body fat while maintaining muscle.",
        "Lean-Bulk": "Slowly gain muscle while keeping fat gain minimal.",
        "Maintain": "Keep your current weight and fitness level.",
        "Flexibility/Mobility": "Enhance movement and flexibility."
    }
    goal = st.selectbox("🎯 Select Your Fitness Goal:", list(goals.keys()), index=list(goals.keys()).index(goal) if goal in goals else 0)
    st.write(f"📌 {goals[goal]}")

    dietary_restriction = st.text_area("🥗 Dietary Restrictions (if any):", dietary_restriction)
    
    if st.button("💾 Save Profile", key="save_button", help="Click to save your profile", use_container_width=True, type="primary"):
        save_user_data(name, height, weight, goal, dietary_restriction)
        st.success("✅ Your details have been saved!")

# AI Trainer - Cbuminator
elif page == "🏋️ Cbuminator":
    st.header("🏋️ Meet Cbuminator - Your Personal AI Trainer")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Cbuminator is your AI-powered gym trainer that helps you improve workouts in real-time.")
        st.write("✅ Detects Posture & Form")
        st.write("✅ Tracks Reps & Sets")
        st.write("✅ Gives Instant Feedback")
        
        # Fitness goals dropdown
        goals = {
            "Bulking": "Increase muscle mass with a calorie surplus.",
            "Cutting": "Reduce body fat while maintaining muscle.",
            "Lean-Bulk": "Slowly gain muscle while keeping fat gain minimal.",
            "Maintain": "Keep your current weight and fitness level.",
            "Flexibility/Mobility": "Enhance movement and flexibility."
        }
        selected_goal = st.selectbox("🎯 Select Your Fitness Goal:", list(goals.keys()))
        st.write(f"📌Current Goal: {goals[selected_goal]}")
        
        # Exercise selection dropdowns
        exercises = ["Bicep Curls", "Yoga", "Pilates", "Squats", "Push-ups", "Deadlifts", "Lunges", "Planks", "Bench Press"]
        selected_exercise = st.selectbox("🏋️ Select Exercise:", exercises)
        # exercise_2 = st.selectbox("🏋️ Select Second Exercise:", exercises)
        
        # Reps selection dropdown
        rep_count = st.selectbox("🔢 Select Rep Count:", list(range(2, 21)))
        
        if st.button("🔥 Start Training", help="Start your journey", use_container_width=True, type="primary"):
            st.success(f"Starting {selected_exercise} for {rep_count} reps... Get moving! 🏋️‍♂️")

            # Run AI_Trainer and capture output
            result = subprocess.run(["python", "AI_God.py", selected_exercise, str(rep_count)], capture_output=True, text=True)
            
            for line in result.stdout.split("\n"):
                if "Score:" in line and "Calories Burned:" in line:
                    parts = line.split("|")
                    score = float(parts[0].split("Score:")[1].strip().replace("%", ""))
                    calories_burned = float(parts[1].split("Calories Burned:")[1].strip())

                    st.write(f"💯 **Your Form Score: {score:.2f}%**")
                    st.write(f"🔥 **Calories Burned: {calories_burned:.2f} kcal**")

            with col2:
                # Read and display the saved chart
                st.write("📊 **Your Form VS Cbum's Form**")
                chart_path = "./database/form_score_chart.png"
                try:
                    image = Image.open(chart_path)
                    st.image(image, caption="Your Form Analysis", use_container_width=True)

                except Exception as e:
                    st.error("Could not load chart. Make sure AI_Trainer.py ran successfully.")

    with col2:
        st_lottie(cbuminator_animation, height=300, key="cbuminator")
    st.sidebar.info("💡 Pro Tip: Ideal rep is 1s-2s push, 1s hold, 4s negative and 1 rest")

# AI Nutritionist - Keto-Kat
elif page == "🥗 Keto-Kat":
    st.header("🥗 Meet Keto-Kat - Your AI Nutritionist")
    col1, col2 = st.columns(2)
    
    with col1:
        # Store detected food items in session state
        if "detected_foods" not in st.session_state:
            st.session_state["detected_foods"] = []

        # Upload Image for Food Recognition
        uploaded_file = st.file_uploader("📸 Upload a food image", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            image_path = "./database/uploaded_food.jpg"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.image(image_path, caption="Uploaded Image", use_column_width=True)

            # Recognize food
            st.write("🔍 Recognizing food items...")
            detected_foods = recognize_food(image_path)
            
            if detected_foods:
                st.session_state["detected_foods"].extend(detected_foods)
                st.success(f"✅ Detected Food Items: {', '.join(detected_foods)}")
                
                # Fetch Nutrition Facts
                st.write("📊 Fetching Nutrition Facts...")
                nutrition_facts = get_nutrition_facts(detected_foods)
                st.write(nutrition_facts)

                # Display Pie Chart
                st.write("📊 **Nutritional Breakdown**")
                
                # Extract macronutrient data
                macro_data = {"Calories": 0, "Proteins": 0, "Fats": 0, "Carbs": 0}
                for line in nutrition_facts.split("\n"):
                    if "calories" in line.lower():
                        macro_data["Calories"] += int("".join(filter(str.isdigit, line)))
                    elif "protein" in line.lower():
                        macro_data["Proteins"] += int("".join(filter(str.isdigit, line)))
                    elif "fat" in line.lower():
                        macro_data["Fats"] += int("".join(filter(str.isdigit, line)))
                    elif "carb" in line.lower():
                        macro_data["Carbs"] += int("".join(filter(str.isdigit, line)))

                # Create a pie chart
                fig, ax = plt.subplots()
                ax.pie(macro_data.values(), labels=macro_data.keys(), autopct='%1.1f%%', startangle=140)
                ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

                # Show pie chart in Streamlit
                st.pyplot(fig)

            else:
                st.error("⚠ No food items detected. Try another image.")

        # Get Meal Plan Button
        if st.button("🍽 Get Meal Plan"):
            if not st.session_state["detected_foods"]:
                st.error("⚠ No detected food items! Please upload a food image first.")
            else:
                st.write("🍳 **Generating Meal Plan based on detected ingredients...**")
                meal_plan = suggest_recipes(st.session_state["detected_foods"])
                st.write(meal_plan)
            
    with col2:
        st_lottie(keto_kat_animation, height=300, key="keto_kat")
    st.sidebar.info("💡 Fun Fact: Chewing gum burns about 11 calories per hour, so technically, you can burn off a stick of gum by just chewing for an hour 😆!")

# Flexpert - Fitness Analytics
elif page == "📊 Flexpert":
    st.header("📊 Your Fitness Journey with Flexpert")
    st.write("Track your **progress** and stay motivated! 📈")
    st.write("🔥 Calories Burned Today: **450 kcal**")
    st.write("🎯 Steps Taken: **8,230 steps**")
    st.write("🏋️‍♂️ Workout Completed: **45 mins**")
    st.progress(85)
    st.sidebar.info("💡 Pro Tip: It takes 21 days to build a habit, but it takes 90 days to build a lifestyle!")

# Footer for all pages - Centered
st.markdown("""
    <style>
        .footer {
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 0px;
            font-size: 16px;
        }
    </style>
    <div class='footer'>
        Made by MacroMind with ❣️
    </div>
""", unsafe_allow_html=True) 

