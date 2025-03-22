# app.py
from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai
from PIL import Image, ImageFile

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-2.0-flash')

def image_resp(prompt : str, image : ImageFile) -> str:
    response = model.generate_content([prompt, image])
    return response.text

def text_resp(prompt : str) -> str:
    response = model.generate_content(prompt)
    return response.text

print(text_resp("who is up tonight?"))
