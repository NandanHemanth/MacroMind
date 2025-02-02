import openai
import os
import base64
from dotenv import load_dotenv
import requests

# Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def encode_image(image_path):
    """Encode image as Base64 for API request."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def recognize_food(image_path):
    """Send image to OpenAI for food recognition."""
    image_base64 = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use available vision-capable model
        messages=[
            {"role": "system", "content": "You are a food recognition expert."},
            {"role": "user", "content": [
                {"type": "text", "text": "Identify all food items in this image and return their nutrition facts."},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"}
            ]}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content if response else "⚠ No food items detected!"

def suggest_recipes(food_items):
    """Suggest recipes based on identified food items."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a recipe expert."},
            {"role": "user", "content": f"Suggest 3 creative recipes using these ingredients: {food_items}"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content if response else "⚠ No recipes found!"

# 🖼 Run on an image file
image_path = "./test.jpg"  # Change to your image path
print("📸 Recognizing food items...")
food_items = recognize_food(image_path)
print("✅ Food Items Identified:\n", food_items)

print("\n🍽 Suggesting Recipes...")
recipes = suggest_recipes(food_items)
print("📜 Recipe Suggestions:\n", recipes)
