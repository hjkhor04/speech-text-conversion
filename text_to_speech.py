from gtts import gTTS
import os
import sys
import tempfile


def text_to_speech(text: str, filename: str = "output.mp3", lang: str = "en", play_now: bool = True):
    """Convert text to speech.

    If play_now is False (default) the function saves the MP3 to `filename`.
    If play_now is True the function will attempt to play audio immediately without keeping a permanent file.

    Playback strategy when play_now=True:
    - First choice: use the offline engine `pyttsx3` (no network, immediate playback).
    - Fallback: save to a temporary MP3 and play it using `playsound` (blocking), then delete the temp file.
    - Final fallback: save to `filename` and call `os.startfile` (may open external player and not block).
    """
    if not text:
        raise ValueError("No text provided for TTS.")

    # If user requested immediate playback, try pyttsx3 first (offline)
    if play_now:
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return
        except Exception:
            # pyttsx3 not available or failed - fall through to temporary-file playback
            pass

        # Use gTTS to create an MP3 in a temporary file, then play it with playsound if available
        tts = gTTS(text=text, lang=lang)
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp_name = tmp.name
        tmp.close()
        try:
            tts.save(tmp_name)
            try:
                # playsound blocks until finished which makes cleanup safe
                from playsound import playsound

                playsound(tmp_name)
                return
            except Exception:
                # playsound not available or failed - fallback to opening the file
                try:
                    os.startfile(tmp_name)
                    print(f"Playing via default app from temporary file: {tmp_name}")
                    return
                except Exception:
                    print(f"Saved temporary TTS to '{tmp_name}'. Please open it to listen.")
                    return
        finally:
            # Attempt to remove the temporary file; if playback is still using it this may fail silently.
            try:
                os.unlink(tmp_name)
            except Exception:
                pass

    # Default behavior: create or overwrite `filename` with the MP3
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    # On Windows, os.startfile will open the MP3 in the default player
    try:
        os.startfile(filename)
    except Exception:
        # Fallback: print location if automatic play fails
        print(f"Saved TTS to '{filename}'. Please open it to listen.")

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         # join all args as the input text
#         input_text = " ".join(sys.argv[1:])
#     else:
#         # fallback text
#         input_text = "Explain Malaysia in 100 words."
#     text_to_speech(input_text)