import os
from gtts import gTTS
from pydub import AudioSegment
from moviepy.config import change_settings

change_settings({"FFMPEG_BINARY": os.getenv("FFMPEG_PATH")})


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')

def generate_audio(commentary):
    if not commentary.strip():
        raise ValueError("No commentary text provided for audio generation.")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    mp3_path = os.path.join(UPLOAD_FOLDER, 'analysis.mp3')
    wav_path = os.path.join(UPLOAD_FOLDER, 'analysis.wav')

    # Remove old files if they exist
    for f in [mp3_path, wav_path]:
        if os.path.exists(f):
            os.remove(f)

    # Generate speech in MP3 format
    tts = gTTS(text=commentary, lang='en')
    tts.save(mp3_path)

    # Convert to WAV
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

    return wav_path
