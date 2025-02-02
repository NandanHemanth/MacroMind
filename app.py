import streamlit as st

# Set page configuration
st.set_page_config(page_title="MacroMind", page_icon="💪", layout="wide")

import requests
import json
import os
import subprocess
import sqlite3
from streamlit_lottie import st_lottie
from PIL import Image
from keto_god import recognize_food, get_nutrition_facts, suggest_recipes, save_meal_data
import matplotlib.pyplot as plt
import json
import plotly.express as px
# Import functions from flexpert_analytics
from flexpert_analytics import (
    load_json_data,
    load_sqlite_data,
    fetch_meal_plan
)

# # Set page configuration
# st.set_page_config(page_title="MacroMind", page_icon="💪", layout="wide")

# Database setup
USER_DATA_PATH = "./database/user_data.json"
EXERCISE_LOG_PATH = "./database/exercise_log.json"
MEAL_PLAN_LOG_PATH = "./database/meal_plan_log.json"
DB_PATH = "./database/user_exercises.db"

def init_user_data():
    """Initialize the user data file if it doesn't exist."""
    os.makedirs(os.path.dirname(USER_DATA_PATH), exist_ok=True)
    
    if not os.path.exists(USER_DATA_PATH):
        default_data = {
            "name": "",
            "height": 170,
            "weight": 70,
            "goal": "",
            "dietary_restriction": ""
        }
        with open(USER_DATA_PATH, "w") as file:
            json.dump(default_data, file, indent=4)

def save_user_data(name, height, weight, goal, dietary_restriction):
    """Saves user data in a JSON file."""
    data = {
        "name": name,
        "height": height,
        "weight": weight,
        "goal": goal,
        "dietary_restriction": dietary_restriction
    }

    with open(USER_DATA_PATH, "w") as file:
        json.dump(data, file, indent=4)

    print("✅ User data saved successfully!")

def load_user_data():
    """Loads user data from the JSON file."""
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, "r") as file:
            try:
                data = json.load(file)
                return (
                    data.get("name", ""),
                    data.get("height", 170),
                    data.get("weight", 70),
                    data.get("goal", ""),
                    data.get("dietary_restriction", "")
                )
            except json.JSONDecodeError:
                print("❌ Error reading user data. Resetting to default values.")
                init_user_data()
    return ("", 170, 70, "", "")

# Initialize User Data
init_user_data()

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
shopping_animation = load_lottie_url('https://lottie.host/bb02a444-4aa8-4fea-bd38-d46fae3b0baf/XDdL3IbPh7.json')  # Healthy shopping animation

# Sidebar Navigation
st.sidebar.title("🚀 MacroMind Menu")
page = st.sidebar.radio("Personal AI Hub", ["🏠 Profile", "🏋️ Cbuminator", "🥗 Keto-Kat", "📊 Flexpert", "🛒 Shopping"])

# Add a space before pet animation for better positioning
st.sidebar.markdown("<br>", unsafe_allow_html=True)
with st.sidebar:
    st_lottie(pet_animation, height=200, key="keto_pet")


# Profile Section
if page == "🏠 Profile":
    st.header("🏠 Your Profile")
    st.write("Enter your details to personalize your fitness journey.")
    
    # Display Profile Picture
    st.markdown("""
        <style>
        .profile-pic {
            display: flex;
            text-align: center;
            justify-content: center;
        }
        img {
            border-radius: 50%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("./assets/profile_pic.jpg", width=150)
    
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

    with col2:
        st.sidebar.info("💡 Fun Fact: You have over 37 trillion cells working together every second to keep you alive—proving that even on your worst days, your body and mind are still fighting for you! 💪🚀")

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
        st.write(f"📌 Current Goal: {goals[selected_goal]}")
        
        # Exercise selection dropdowns
        exercises = ["Bicep Curls", "Yoga", "Pilates", "Squats", "Push-ups", "Deadlifts", "Lunges", "Planks", "Bench Press"]
        selected_exercise = st.selectbox("🏋️ Select Exercise:", exercises)
        
        # Reps selection dropdown
        rep_count = st.selectbox("🔢 Select Rep Count:", list(range(2, 21)))
        
        if st.button("🔥 Start Training", help="Start your journey", use_container_width=True, type="primary"):
            st.success(f"Starting {selected_exercise} for {rep_count} reps... Get moving! 🏋️‍♂️")

            # Run AI_God.py and capture output
            result = subprocess.run(["python", "AI_God.py", selected_exercise, str(rep_count)], capture_output=True, text=True)
            
            # Extract relevant data from output
            score, calories_burned = None, None
            for line in result.stdout.split("\n"):
                if "Score:" in line and "Calories Burned:" in line:
                    parts = line.split("|")
                    try:
                        score = float(parts[0].split("Score:")[1].strip().replace("%", ""))
                        calories_burned = float(parts[1].split("Calories Burned:")[1].strip())
                    except (IndexError, ValueError):
                        st.error("Error parsing workout data. Please try again.")

            # Display results
            if score is not None and calories_burned is not None:
                st.write(f"💯 **Your Form Score: {score:.2f}%**")
                st.write(f"🔥 **Calories Burned: {calories_burned:.2f} kcal**")

            # Display Form Score Chart
            with col2:
                st.write("📊 **Your Form VS Cbum's Form**")
                chart_path = "./database/form_score_chart.png"
                try:
                    image = Image.open(chart_path)
                    st.image(image, caption="Your Form Analysis", use_container_width=True)
                except Exception:
                    st.error("⚠ Could not load chart. Make sure AI_God.py ran successfully.")

    with col2:
        st_lottie(cbuminator_animation, height=300, key="cbuminator")
    
    st.sidebar.info("💡 Pro Tip: Ideal rep is 1s-2s push, 1s hold, 4s negative and 1s rest.")

# AI Nutritionist - Keto-Kat
elif page == "🥗 Keto-Kat":
    st.header("🥗 Meet Keto-Kat - Your AI Nutritionist")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Personalized meal plans, dietary tracking, and health recommendations!")
        st.write("🍎 Tracks Macros & Calories")
        st.write("🥑 Suggests Meals Based on Fitness Goals")
        st.write("💧 Hydration & Supplements Advice")
        # Store detected food items in session state
        if "detected_foods" not in st.session_state:
            st.session_state["detected_foods"] = []

        # Upload Image for Food Recognition
        uploaded_file = st.file_uploader("📸 Upload a food image", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            image_path = "./database/uploaded_food.jpg"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.image(image_path, caption="Uploaded Image", use_container_width=True)

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
                
                # Extract macronutrient data safely
                macro_data = {"Calories": 0, "Proteins": 0, "Fats": 0, "Carbs": 0}

                for line in nutrition_facts.split("\n"):
                    digits = "".join(filter(str.isdigit, line))  # Extract only digits

                    if digits:  # Check if digits exist before conversion
                        value = int(digits)
                        if "calories" in line.lower():
                            macro_data["Calories"] += value
                        elif "protein" in line.lower():
                            macro_data["Proteins"] += value
                        elif "fat" in line.lower():
                            macro_data["Fats"] += value
                        elif "carb" in line.lower():
                            macro_data["Carbs"] += value

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
            # Save the generated meal data
            save_meal_data(
                detected_foods=st.session_state["detected_foods"],
                nutrition_facts=get_nutrition_facts(st.session_state["detected_foods"]),
                meal_plan=meal_plan
            )
            
    with col2:
        st_lottie(keto_kat_animation, height=300, key="keto_kat")
    st.sidebar.info("💡 Fun Fact: Chewing gum burns about 11 calories per hour, so technically, you can burn off a stick of gum by just chewing for an hour 😆!")

# Flexpert - Fitness Analytics
elif page == "📊 Flexpert":
    st.header("📊 Your Fitness Journey with Flexpert")

    st.write("Track your **progress** and stay motivated! 📈")
    st.write("🔥 Calories Burned Today: **450 kcal**")
    st.write("🎯 Steps Taken: **1230 steps**")
    st.write("🏋️‍♂️ Workout Completed: **45 mins**")

    st.progress(35)  # Fitness Goal Completion Bar

    # Load user data
    exercise_log = load_json_data(EXERCISE_LOG_PATH)
    user_data = load_json_data(USER_DATA_PATH)
    exercise_df = load_sqlite_data()    

    # Extract user details
    fitness_goal = user_data.get("goal", "Maintain")
    detected_foods = [log["exercise_name"] for log in exercise_log]

    if st.button("📋 Give me my complete plan"):
        with st.spinner("🔄 Generating your complete plan... Please wait!"):
            # Fetch AI-generated meal plan
            meal_plan = fetch_meal_plan(detected_foods, fitness_goal)
            
            # # Generate workout streak calendar
            # workout_dates = [log["timestamp"].split(" ")[0] for log in exercise_log]
            # streak_calendar = generate_calendar(workout_dates)

            st.success("✅ Your complete plan is ready!")

            # Display meal plan
            st.subheader("🍽 Customized Meal Plan")
            st.write(meal_plan)

            # Display workout streak calendar
            st.subheader("📅 Workout Streaks")
            # st.text(streak_calendar)

            # Display analytics charts
            st.subheader("📊 Workout Performance")

            fig1 = px.bar(exercise_df, x="timestamp", y="calories", color="exercise_name", title="Calories Burned Over Time")
            st.plotly_chart(fig1)

            fig2 = px.line(exercise_df, x="timestamp", y="score", color="exercise_name", title="Workout Form Scores Over Time")
            st.plotly_chart(fig2)

    st.sidebar.info("💡 Stay consistent! Track your workouts and diet to maximize results.")


# Shopping Section
elif page == "🛒 Shopping":
    st.header("🛒 Smart Grocery Shopping for a Healthier You")
    st.write("Plan your grocery shopping based on AI-suggested meals and healthier food choices!")

    col1, col2 = st.columns([2, 1])  # Make col1 larger for the table
    
    # Animation in Column 2
    with col2:
        st_lottie(shopping_animation, height=300, key="shopping_animation")

    with col1:
        st.write("🥦 **Shop Smart & Stay Healthy!**")
        st.write("✅ Plan groceries based on AI-generated meal plans.")
        st.write("✅ Get **better alternatives** for unhealthy items.")
        st.write("✅ Find the best deals on healthy ingredients.")

        # Smart Shop Button
        if st.button("🛍 Smart Shop", key="smart_shop", help="Click to generate your shopping checklist with AI recommendations"):
            with st.spinner("🔄 Generating your AI-powered grocery checklist..."):
                from shopping import load_meal_plan_log, generate_grocery_list, create_grocery_table

                # Load meal plans
                meal_plan_log = load_meal_plan_log()

                if not meal_plan_log:
                    st.warning("⚠ No meal plans found! Generate a meal plan first.")
                else:
                    latest_meal_plan = meal_plan_log[-1]["meal_plan"]  # Get the most recent meal plan
                    grocery_list = generate_grocery_list(latest_meal_plan)

                    if grocery_list.startswith("❌"):
                        st.error(grocery_list)
                    else:
                        grocery_df = create_grocery_table(grocery_list)

                        st.success("✅ Your grocery checklist is ready!")

                        # Full-width table spanning both columns
                        st.subheader("📝 Your AI-Generated Grocery List")
                        st.dataframe(grocery_df, width=1000)

                        # Add checkboxes for interactive shopping
                        checked_items = []
                        for index, row in grocery_df.iterrows():
                            checked = st.checkbox(f"{row['Item']}", key=row['Item'])
                            if checked:
                                checked_items.append(row['Item'])

                        st.write(f"✅ {len(checked_items)} / {len(grocery_df)} items checked")

                        # Display nutrition facts
                        st.subheader("🥗 Nutrition Facts for Your Ingredients")
                        from keto_god import get_nutrition_facts
                        nutrition_facts = get_nutrition_facts([row['Item'] for _, row in grocery_df.iterrows()])
                        st.write(nutrition_facts)

                        # Display shopping links
                        st.subheader("🛍 Shop Your Groceries Online")
                        for index, row in grocery_df.iterrows():
                            st.markdown(f"🔗 [Find **{row['Item']}** on Wakefern]({row['Wakefern Link']})")

    st.sidebar.info("💡 AI-powered shopping helps you stay on track with your health goals!")

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

