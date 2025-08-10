import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def detect_language_gemini(audio_file_path: str):
    """
    Detects the language spoken in an audio file using Google Gemini.
    Returns language code like 'en', 'hi', 'ta'.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        model = genai.GenerativeModel("gemini-2.5-pro")  

        prompt = "Detect the spoken language code (en, hi, ta, etc.) in this audio. Only return the code."
        response = model.generate_content([
            {"mime_type": "audio/wav", "data": audio_data},
            prompt
        ])

        return response.text.strip()

    except Exception as e:
        print(f"[Gemini Connector Error] {e}")
        return None
