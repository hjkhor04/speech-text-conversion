from speech_to_text import listen_from_mic
from google import genai
from gemini import generate_gemini_response
from text_to_speech import text_to_speech

if __name__ == "__main__":
    prompt_text = listen_from_mic()
    response_text = generate_gemini_response(prompt_text)
    print("🤖 Gemini Response:")
    print(response_text)
    text_to_speech(response_text, play_now=True)