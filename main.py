# # from connectors.gemini_connector import detect_language_gemini
# from connectors.openAI_connector import detect_language_openai


# #audio file
# audio_path = "Recording.mp3"  # or .mp3

# #function
# # language_code = detect_language_gemini(audio_path)
# language_code = detect_language_openai(audio_path)

# print(f"Detected language code: {language_code}")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from coordination.coordination import run_all_providers

app = FastAPI()

class LanguageDetectionRequest(BaseModel):
    audio_file_path: str
    ground_truth_language: str  #testing context

@app.post("/detect/language")
def detect_language(request: LanguageDetectionRequest):
    """
    Detects spoken language from an audio file using all 4 providers.
    """
    # Validate file exists
    if not os.path.isfile(request.audio_file_path):
        raise HTTPException(
            status_code=400,
            detail=f"Audio file not found: {request.audio_file_path}"
        )

    try:
        results = run_all_providers(request.audio_file_path)
        return {
            "ground_truth_language": request.ground_truth_language,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
