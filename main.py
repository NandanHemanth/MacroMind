import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie

# Set page config
st.set_page_config(page_title="MacroMind", page_icon="💪", layout="wide")

# Load Lottie Animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

ai_trainer_animation = load_lottie_url("https://assets4.lottiefiles.com/private_files/lf30_3X1oGR.json")  # Example Lottie Animation
nutrition_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_V9t630.json")  # Example Lottie Animation

# Sidebar Navigation
st.sidebar.title("🚀 MacroMind Menu")
page = st.sidebar.radio("Choose a Section:", ["🏋️ AI Trainer - Samuelek", "🥗 AI Nutritionist", "📊 Progress & Analytics"])

# Home Section
st.title("MacroMind - Your AI Fitness & Nutrition Hub 🎯")
st.subheader("Welcome to MacroMind! Let's get you fit & healthy in a fun, engaging way!")

# **1️⃣ AI Trainer - Samuelek**
if page == "🏋️ AI Trainer - Samuelek":
    st.header("🏋️ Meet Samuelek - Your Personal AI Trainer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Samuelek is your AI-powered gym trainer that helps you improve workouts in real-time.")
        st.write("✅ Detects Posture & Form")
        st.write("✅ Tracks Reps & Sets")
        st.write("✅ Gives Instant Feedback")

        # Start Workout Button
        if st.button("🔥 Start Training"):
            st.success("Tracking workout... Get ready! 🏋️‍♂️")

    with col2:
        st_lottie(ai_trainer_animation, height=300)

# **2️⃣ AI Nutritionist Section**
elif page == "🥗 AI Nutritionist":
    st.header("🥗 AI-Powered Nutritionist")

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Personalized meal plans, dietary tracking, and health recommendations!")
        st.write("🍎 Tracks Macros & Calories")
        st.write("🥑 Suggests Meals Based on Fitness Goals")
        st.write("💧 Hydration & Supplements Advice")

        # Meal Suggestion Button
        if st.button("🍽 Get Meal Plan"):
            st.success("Fetching your personalized meal plan... 🍕")

    with col2:
        st_lottie(nutrition_animation, height=300)

# **3️⃣ Progress & Analytics Section**
elif page == "📊 Progress & Analytics":
    st.header("📊 Your Fitness Journey")

    st.write("Track your **progress** and stay motivated! 📈")
    st.write("🔥 Calories Burned Today: **450 kcal**")
    st.write("🎯 Steps Taken: **8,230 steps**")
    st.write("🏋️‍♂️ Workout Completed: **45 mins**")

    st.progress(85)  # Fitness Goal Completion Bar

st.sidebar.info("💡 Pro Tip: Use AI Trainer for live posture tracking!")
