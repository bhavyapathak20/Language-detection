import os
from sarvamai import SarvamAI
from dotenv import load_dotenv

load_dotenv()
SARVAMAI_API_KEY = os.getenv("SARVAMAI_API_KEY")

client = SarvamAI(api_subscription_key=SARVAMAI_API_KEY)

def detect_language_sarvamAI(audio_file_path: str):
    """
    Detects the language spoken in an audio file using OpenAI's transcription API.
    Returns language code like 'en', 'hi', 'ta'.
    """
    try:
        with open(audio_file_path, "rb") as f:
            response = client.speech_to_text.transcribe(
                file=f,
                model="saarika:v2.5",
            )
        
        return response.language_code

    except Exception as e:
        print(f"[Sarvam Connector Error] {e}")
        return None
    
# if __name__ == "__main__":
#     audio_file = "Recording.mp3"
#     lang_code = detect_language_sarvamAI(audio_file)
#     print(f"Detected language code (Sarvam AI): {lang_code}")
