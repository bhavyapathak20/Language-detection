import time
import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connectors.openAI_connector import detect_language_openai
from connectors.gemini_connector import detect_language_gemini
from connectors.sarvamAI_connector import detect_language_sarvamAI
from connectors.elevenLabs_connector import detect_language_elevenlabs

def run_all_providers(audio_file_path: str):
    providers = [
        ("OpenAI", detect_language_openai, 0.002),
        ("Google Gemini", detect_language_gemini, 0.0015),
        ("SarvamAI", detect_language_sarvamAI, 0.001),
        ("ElevenLabs", detect_language_elevenlabs, 0.0025)
    ]

    results = []

    for name, func, cost_per_request in providers:
        start_time = time.time()
        status = "success"
        lang_code = None
        error_message = None

        # Capture print output from connector
        buffer = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buffer

        try:
            lang_code = func(audio_file_path)
            if not lang_code:
                status = "failure"
        except Exception as e:
            status = "error"
            error_message = str(e)
        finally:
            sys.stdout = sys_stdout
            printed_output = buffer.getvalue().strip()
            buffer.close()

        # If no exception but something was printed, treat it as error message
        if printed_output and not error_message:
            error_message = printed_output

        end_time = time.time()

        results.append({
            "provider": name,
            "detected_language": lang_code,
            "time_taken_sec": round(end_time - start_time, 2),
            "estimated_cost_usd": cost_per_request,
            "status": status,
            "error_message": error_message
        })

    return results

if __name__ == "__main__":
    file_path = "Recording.mp3"
    report = run_all_providers(file_path)
    for r in report:
        print(r)
