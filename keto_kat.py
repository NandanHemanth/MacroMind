import openai
import cv2
import json
import os
import pytesseract
import numpy as np
import sqlite3
from pyzbar.pyzbar import decode
from PIL import Image
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_PATH = "./database/user_data.db"

def get_user_data():
    """Fetch user fitness goal and dietary restriction from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT goal, dietary_restriction FROM user_profile WHERE id=1")
    data = cursor.fetchone()
    conn.close()
    return data if data else ("Maintain", "None")

def draw_rectangle(frame):
    """Draws a rectangle in the center of the frame to position food items or barcodes."""
    height, width, _ = frame.shape
    start_point = (int(width * 0.3), int(height * 0.3))
    end_point = (int(width * 0.7), int(height * 0.7))
    color = (0, 255, 0)
    thickness = 2
    cv2.rectangle(frame, start_point, end_point, color, thickness)
    return frame

def analyze_food_image():
    """Captures an image from the webcam and analyzes it for nutritional content."""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print("Press space to capture the image.")
    while True:
        ret, frame = cap.read()
        frame = draw_rectangle(frame)
        cv2.imshow("Capture Food Image", frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    img_path = "captured_food.jpg"
    cv2.imwrite(img_path, frame)
    print("Image captured successfully!")
    
    text = pytesseract.image_to_string(frame)
    print("Extracted Text:", text)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a nutrition expert."},
            {"role": "user", "content": f"Analyze the nutritional facts from this food label text: {text}"}
        ]
    )
    
    nutrition_info = response["choices"][0]["message"]["content"]
    print("Nutritional Analysis:", nutrition_info)
    
    return nutrition_info

def scan_barcode():
    """Scans a barcode and fetches nutritional facts."""
    cap = cv2.VideoCapture(0)
    print("Position the barcode inside the green box.")
    
    while True:
        ret, frame = cap.read()
        frame = draw_rectangle(frame)
        cv2.imshow("Scan Barcode", frame)
        
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    decoded_objects = decode(image)
    
    if not decoded_objects:
        print("No barcode detected.")
        return
    
    barcode_data = decoded_objects[0].data.decode('utf-8')
    print("Scanned Barcode:", barcode_data)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in food nutrition."},
            {"role": "user", "content": f"Find the nutritional details for this barcode: {barcode_data}"}
        ]
    )
    
    nutrition_info = response["choices"][0]["message"]["content"]
    print("Nutritional Information:", nutrition_info)
    
    return nutrition_info

if __name__ == "__main__":
    import sys
    
    task = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if task == "1":
        analyze_food_image()
    elif task == "2":
        scan_barcode()
    else:
        print("Invalid option. Use 1 for photo analysis, 2 for barcode scanning.")