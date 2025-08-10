# Multi-Provider Language Detection API

This project provides a **FastAPI-based REST API** that detects the spoken language from an audio file using **four different AI providers**:
```
NOTE : 3 out of 4 connectors are fully implemented, openAI key quota has been finished
```

- **OpenAI**
- **Google Gemini**
- **SarvamAI**
- **ElevenLabs**

The results from all providers are aggregated into a single JSON response with:
- Detected language code (e.g., `en`, `hi`, `ta`)
- Time taken for each provider
- Estimated cost per request
- Status (success/failure/error)
- Error messages (if any)

---

## 🚀 How It Works

## 1. **Connectors**
Each provider has its own connector in the `connectors/` folder:
- `openAI_connector.py` — Uses Whisper for transcription + GPT-4o-mini for language detection.
- `gemini_connector.py` — Uses Google Gemini to directly detect the language from audio.
- `sarvamAI_connector.py` — Uses SarvamAI transcription service to get the detected language.
- `elevenLabs_connector.py` — Uses ElevenLabs Speech-to-Text to detect the language.

Each connector exposes a function:
```python
detect_language_<provider>(audio_file_path: str) -> str | None
```
which returns the language code or None if detection fails.

## 2. **Coordination Layer**
coordination/coordination.py contains:

```bash
run_all_providers(audio_file_path: str)
```
calls all four connectors, records time taken, cost, status, and errors, and returns a list of results.

## 3. **FastAPI Application**
main.py defines:

```
POST /detect/language
```
 takes JSON input with:

```bash
{
  "audio_file_path": "path/to/file.mp3",
  "ground_truth_language": "en"
}
```
**audio_file_path:** Local path to the audio file.

**ground_truth_language:** Used only for reference in the response.

Returns:

```
{
  "ground_truth_language": "en",
  "results": [
    {
      "provider": "OpenAI",
      "detected_language": "en",
      "time_taken_sec": 1.23,
      "estimated_cost_usd": 0.002,
      "status": "success",
      "error_message": null
    },
    ...
  ]
}
```

# 📂 Project Structure
```
DripLink-pyTask/
├── connectors/
│   ├── openAI_connector.py
│   ├── gemini_connector.py
│   ├── sarvamAI_connector.py
│   ├── elevenLabs_connector.py
│
├── coordination/
│   ├── coordination.py
│   ├── __init__.py
│
├── main.py
├── .env
└── README.md
```

## 🔑 Environment Variables
Create a .env file in the project root:

```OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
SARVAMAI_API_KEY=your_sarvamai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

# 🛠 Steps to Run
- ### **Clone the repository**

```git clone <repo-url>
cd DripLink-pyTask
```

- ### **Install dependencies**

```
pip install fastapi uvicorn python-dotenv openai google-generativeai sarvamai elevenlabs
```

- ### **Add your API keys in .env**

- ### **Start the FastAPI server**


```
python -m uvicorn main:app --reload
```

- ### **Open Swagger UI**

- **Visit:**
```
http://127.0.0.1:8000/docs
```

- ### **Test the /detect/language endpoint**

# ⚙️ How FastAPI Works Here
FastAPI is a Python web framework for building APIs quickly.

The **@app.post("/detect/language")** registers a POST endpoint.


### **On a request, FastAPI:**

```
Parses JSON → creates a LanguageDetectionRequest object.

Passes audio_file_path to run_all_providers.

Aggregates results from all connectors.

Returns them as a JSON response.
```

# 🧪 Example Request (via Swagger)
```
{
  "audio_file_path": "C:/Users/Bhavya Pathak/OneDrive/Documents/Sound Recordings/Test.mp3",
  "ground_truth_language": "hi"
}
```
# 📝 Notes
Use forward slashes / or escaped backslashes \\ in Windows paths.

All providers require valid API keys in .env.

This API does not upload the audio, it reads it directly from your local file system.
