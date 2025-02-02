import os
import requests
import base64
from dotenv import load_dotenv
import json

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Updated Gemini API Endpoint
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def encode_image(image_path):
    """Encodes an image to Base64 for API request."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def recognize_food(image_path):
    """Recognizes food items in an image using Gemini AI."""
    image_base64 = encode_image(image_path)
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}},
                {"text": "List all food items present in this image."}
            ]
        }]
    }

    response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        detected_foods = result["candidates"][0]["content"]["parts"][0]["text"]
        return detected_foods.split(", ")  # Convert string to list
    else:
        return []

def get_nutrition_facts(food_items):
    """Fetches nutrition facts for detected foods using Gemini AI."""
    query = f"Provide detailed nutrition facts for these food items: {', '.join(food_items)}."
    
    data = {"contents": [{"parts": [{"text": query}]}]}
    response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "❌ Error fetching nutrition facts."

def suggest_recipes(food_items):
    """Generates recipes using detected food items."""
    query = f"Suggest 3 recipes using these ingredients: {', '.join(food_items)}."

    data = {"contents": [{"parts": [{"text": query}]}]}
    response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "❌ Error fetching recipes."
    
def save_meal_data(detected_foods, nutrition_facts, meal_plan):
    """Saves meal data (detected foods, nutrition, and meals) to a JSON file."""
    data = {
        "detected_foods": detected_foods,
        "nutrition_facts": nutrition_facts,
        "meal_plan": meal_plan
    }

    file_path = "./database/meal_data.json"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Load existing data if file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Append new meal data
    existing_data.append(data)

    # Save back to file
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

    print("✅ Meal data saved successfully!")

# Testing with the Fridge pic
# def main(image_path):
#     print("📸 Recognizing food items...")
#     food_items = recognize_food(image_path)
    
#     if not food_items:
#         print("⚠ No food items detected!")
#         return

#     print(f"✅ Detected Food Items: {', '.join(food_items)}")
    
#     print("\n📊 Fetching Nutrition Facts...")
#     nutrition_facts = get_nutrition_facts(food_items)
#     print(nutrition_facts)

#     print("\n🍽 Suggesting Recipes...")
#     recipes = suggest_recipes(food_items)
#     print(recipes)

# # Run the script with your image file
# if __name__ == "__main__":
#     image_path = "./fridge.jpg"  # Change this to your image path
#     main(image_path)
