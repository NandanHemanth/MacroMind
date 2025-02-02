import streamlit as st
import json
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API key for Gemini AI
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# File path for meal plan logs
MEAL_PLAN_LOG_PATH = "./database/meal_plan_log.json"

def load_meal_plan_log():
    """Loads the meal plan log from JSON file."""
    if os.path.exists(MEAL_PLAN_LOG_PATH):
        with open(MEAL_PLAN_LOG_PATH, "r") as file:
            return json.load(file)
    return []

def generate_grocery_list(meal_plan):
    """Uses Gemini AI to convert meal plan into a structured grocery list."""
    query = f"Extract and categorize ingredients from this meal plan into a structured grocery shopping list: {meal_plan}."
    data = {"contents": [{"parts": [{"text": query}]}]}
    response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=data)

    if response.status_code == 200:
        grocery_list = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return grocery_list
    return "❌ Error generating grocery list."

def create_grocery_table(grocery_list):
    """Converts AI-generated grocery list into a DataFrame."""
    items = grocery_list.split("\n")  # Assume items are line-separated
    grocery_data = {"Item": [], "Wakefern Link": []}

    for item in items:
        item_name = item.strip()
        if item_name:
            wakefern_url = f"https://www2.wakefern.com/search?q={item_name.replace(' ', '+')}"
            grocery_data["Item"].append(item_name)
            grocery_data["Wakefern Link"].append(wakefern_url)

    return pd.DataFrame(grocery_data)

# Streamlit UI
st.header("🛒 AI-Generated Grocery Checklist")
st.write("Automatically extracted from your **meal plans**!")

# Load meal plans
meal_plan_log = load_meal_plan_log()

if not meal_plan_log:
    st.warning("⚠ No meal plans found! Generate a meal plan first.")
else:
    latest_meal_plan = meal_plan_log[-1]["meal_plan"]  # Get most recent meal plan
    grocery_list = generate_grocery_list(latest_meal_plan)

    if grocery_list.startswith("❌"):
        st.error(grocery_list)
    else:
        grocery_df = create_grocery_table(grocery_list)
        st.write("📝 **Your Grocery List**")
        st.dataframe(grocery_df, width=800)

        # Add checkboxes for interactive shopping
        checked_items = []
        for index, row in grocery_df.iterrows():
            checked = st.checkbox(f"{row['Item']}", key=row['Item'])
            if checked:
                checked_items.append(row['Item'])

        st.write(f"✅ {len(checked_items)} / {len(grocery_df)} items checked")

        st.write("🛍 **Click on the links below to shop for groceries on Wakefern:**")
        for index, row in grocery_df.iterrows():
            st.markdown(f"🔗 [Shop for **{row['Item']}**]({row['Wakefern Link']})")

st.sidebar.info("💡 AI-powered shopping helps you stay on track with your health goals!")
