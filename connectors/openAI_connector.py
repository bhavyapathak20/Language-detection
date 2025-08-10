import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def detect_language_openai(audio_file_path: str):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        text = transcription.text

        lang_detect = client.responses.create(
            model="gpt-4o-mini",
            input=f"Detect the language code (like en, hi, ta) for this text: {text}. Only return the code."
        )

        return lang_detect.output_text.strip()

    except Exception as e:
        print(f"[OpenAI Connector Error] {e}")
        return None