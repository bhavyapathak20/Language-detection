import os
from dotenv import load_dotenv
from io import BytesIO
from elevenlabs import ElevenLabs


load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def detect_language_elevenlabs(audio_file_path: str):
    """
    Detects the language spoken in an audio file using ElevenLabs Speech-to-Text.
    Returns a language code like 'en', 'hi', 'ta', or None on error.
    """
    try:
        with open(audio_file_path, "rb") as f:
            audio_bytes = BytesIO(f.read())

        response = client.speech_to_text.convert(
            file=audio_bytes,
            model_id="scribe_v1"
        )

        return response.language_code

    except Exception as e:
        print(f"Error: {e}")
        return None

# if __name__ == "__main__":
#     audio_file = "Recording.mp3"  
#     lang_code = detect_language_elevenlabs(audio_file)
#     print(f"Detected language code (ElevenLabs AI): {lang_code}")
