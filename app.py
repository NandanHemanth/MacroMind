import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Set page configuration
st.set_page_config(page_title="MacroMind", page_icon="💪", layout="wide")

# Function to load Lottie animations from a URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations from URLs
keto_kat_animation = load_lottie_url('https://lottie.host/89ed7481-222e-4850-879d-a96471c32534/3hVtb56VQF.json')  # Cat with food
cbuminator_animation = load_lottie_url('https://lottie.host/0aa94491-176f-4cfd-a7a3-48fdc2cbc844/A3C89do9KL.json')  # Workout theme

# Sidebar Navigation
st.sidebar.title("🚀 MacroMind Menu")
page = st.sidebar.radio("Personal AI Hub", ["🏋️ Cbuminator", "🥗 Keto-Kat", "📊 Flexpert"])

# Home Section
st.title("MacroMind - Your AI Fitness & Nutrition Hub 🎯")
# st.subheader("Welcome to MacroMind! Let's get you fit & healthy in a fun, engaging way!")

# AI Trainer - Cbuminator
if page == "🏋️ Cbuminator":
    st.header("🏋️ Meet Cbuminator - Your Personal AI Trainer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Cbuminator is your AI-powered gym trainer that helps you improve workouts in real-time.")
        st.write("✅ Detects Posture & Form")
        st.write("✅ Tracks Reps & Sets")
        st.write("✅ Gives Instant Feedback")

        # Start Workout Button
        if st.button("🔥 Start Training"):
            st.success("Tracking workout... Get ready! 🏋️‍♂️")

    with col2:
        st_lottie(cbuminator_animation, height=300, key="cbuminator")

    st.sidebar.info("💡 Pro Tip: Maintaining proper posture during workouts is more important than higher weights for maximum gains 💪🔥")

# AI Nutritionist - Keto-Kat
elif page == "🥗 Keto-Kat":
    st.header("🥗 Meet Keto-Kat - Your AI Nutritionist")

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
        st_lottie(keto_kat_animation, height=300, key="keto_kat")

    st.sidebar.info("💡 Fun Fact: Chewing gum burns about 11 calories per hour, so technically, you can burn off a stick of gum by just chewing for an hour 😆!")

# Flexpert - Fitness Analytics
elif page == "📊 Flexpert":
    st.header("📊 Your Fitness Journey with Flexpert")

    st.write("Track your **progress** and stay motivated! 📈")
    st.write("🔥 Calories Burned Today: **450 kcal**")
    st.write("🎯 Steps Taken: **8,230 steps**")
    st.write("🏋️‍♂️ Workout Completed: **45 mins**")

    st.progress(85)  # Fitness Goal Completion Bar

    st.sidebar.info("💡 Pro Tip: It takes 21 days to build a habbit, but it takes 90 days to build a lifestyle!")

# st.sidebar.info("💡 Pro Tip: Use Cbuminator for live posture tracking!")
