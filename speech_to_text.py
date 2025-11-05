import speech_recognition as sr
from pathlib import Path

recognizer = sr.Recognizer()

def listen_from_mic(callback=None):
    """
    Continuously listens to speech from the microphone.
    If a callback is provided, recognized text will be passed to it.
    Otherwise, prints the recognized text.
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening... Speak clearly.")
        while True:
            try:
                # Capture audio
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)

                # Convert speech to text
                text = recognizer.recognize_google(audio)
                print(f"🗣️ Recognized: {text}")

                # If a callback function is provided, send the text to it
                if callback:
                    callback(text)
                else:
                    # If no callback supplied, return the text from a single listen
                    # (caller should call this function and break the loop if they want one-shot)
                    return text

            except sr.UnknownValueError:
                print("⚠️ Didn't catch that. Please repeat.")
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
            except KeyboardInterrupt:
                print("\n🛑 Exiting speech recognition...")
                break

if __name__ == "__main__":
    # Example: Just print recognized text
    listen_from_mic()


def listen_once() -> str:
    """Listen once from the default microphone and return the recognized text.

    Returns an empty string if nothing was recognized. Raises RuntimeError on API errors.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        raise RuntimeError(f"Speech API request failed: {e}") from e


def transcribe_file(path: str) -> str:
    """Transcribe a given audio file and return the recognized text string.

    Supports WAV and other formats supported by SpeechRecognition's AudioFile.
    Returns empty string when nothing recognized; raises RuntimeError on API failures.
    """
    p = Path(path)
    if not p.exists():
        raise RuntimeError(f"File not found: {path}")

    r = sr.Recognizer()
    try:
        with sr.AudioFile(str(p)) as source:
            audio = r.record(source)
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        raise RuntimeError(f"Speech API request failed: {e}") from e
