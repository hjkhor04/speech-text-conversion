from google import genai
from speech_to_text import listen_from_mic

GEMINI_API_KEY = "YOUR API KEY HERE"
# The client gets the API key from the environment variable `GEMINI_API_KEY`.

def generate_gemini_response(prompt_text: str) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt_text
    )
    return response.text

