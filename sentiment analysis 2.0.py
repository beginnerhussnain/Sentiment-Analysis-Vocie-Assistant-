import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS
import os
import pygame

# Define the relative path to the theme file
THEME_PATH = "AI Projects/Camera gestures/azure.tcl"

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        status_label.config(text="Listening...")
        window.update_idletasks()
        audio = recognizer.listen(source)

    try:
        transcript = recognizer.recognize_google(audio)
        status_label.config(text="Speech recognized")
        return transcript
    except sr.RequestError:
        status_label.config(text="API unavailable")
        return None
    except sr.UnknownValueError:
        status_label.config(text="Unable to recognize speech")
        return None

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment

def get_emotion(polarity):
    if polarity > 0.5:
        return "Happy 😊"
    elif 0 < polarity <= 0.5:
        return "Neutral 🙂"
    elif -0.5 <= polarity < 0:
        return "Sad 😔"
    else:
        return "Depressed 😢"

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for the audio to finish playing
        continue

def on_analyze_button_click():
    transcript = recognize_speech_from_mic()
    if transcript:
        text_area.insert(tk.END, f"User: {transcript}\n")
        sentiment = analyze_sentiment(transcript)
        emotion = get_emotion(sentiment.polarity)
        
        sentiment_output = f"Emotion: {emotion}\n"
        text_area.insert(tk.END, f"AI: {sentiment_output}\n")
        
        # Generate audio output for sentiment and emotion
        response = f"The detected emotion is {emotion}."
        audio_file = "response.mp3"
        tts = gTTS(response)
        tts.save(audio_file)
        play_audio(audio_file)
        os.remove(audio_file)

# Create the main window
window = tk.Tk()
window.title("Sentiment and Emotion Analysis with Voice Input")
window.geometry("600x500")
window.resizable(False, False)

# Apply the azure theme
style = ttk.Style(window)
if os.path.exists(THEME_PATH):
    window.tk.call("source", THEME_PATH)
    style.theme_use("azure")
else:
    print(f"Theme file not found at {THEME_PATH}. Using default theme.")

# Create a frame for the status label and button
top_frame = ttk.Frame(window, padding=10)
top_frame.pack(fill=tk.X)

status_label = ttk.Label(top_frame, text="Click 'Analyze' to start", font=("Helvetica", 14))
status_label.pack(side=tk.LEFT, padx=10)

analyze_button = ttk.Button(top_frame, text="Analyze", command=on_analyze_button_click)
analyze_button.pack(side=tk.RIGHT, padx=10)

# Create a scrolled text widget to display the conversation
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Consolas", 12), width=70, height=20)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Add credits footer
footer_label = ttk.Label(window, text="Developed with ♥ using Python", font=("Helvetica", 10), anchor=tk.CENTER)
footer_label.pack(pady=5)

# Start the GUI event loop
window.mainloop()