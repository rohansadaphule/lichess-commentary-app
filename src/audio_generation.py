import pyttsx3
import os

def generate_audio(text):
    engine = pyttsx3.init()
    
    # Configure the speech engine
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    # Generate audio file
    output_path = os.path.join('..', 'uploads', 'commentary.mp3')
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    
    return output_path