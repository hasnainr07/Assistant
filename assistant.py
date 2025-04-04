import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import requests
import pywhatkit as kit
import pyautogui

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    """ Convert text to speech """
    engine.say(audio)
    engine.runAndWait()

def take_command():
    """ Recognizes speech input from the microphone """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand the audio, please repeat.")
            return "None"
        except sr.RequestError:
            print("Could not request results, check your internet connection.")
            return "None"

def process_command(query):
    """ Process the voice command """

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        results = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
        print(results)
        speak(results)

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")

    elif "search google" in query:
        speak("What should I search?")
        search_query = take_command()
        if search_query != "none":
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

    elif "play music" in query:
        music_dir = 'E:\\Musics'  # Change this to your music folder
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, random.choice(songs)))

    elif "the time" in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {str_time}")

    elif "shutdown system" in query:
        os.system("shutdown /s /t 5")

    elif "restart system" in query:
        os.system("shutdown /r /t 5")

    elif "take screenshot" in query:
        speak("Tell me a name for the file")
        file_name = take_command()
        if file_name != "none":
            pyautogui.screenshot().save(f"{file_name}.png")
            speak("Screenshot saved")

if __name__ == "__main__":
    speak("Assistant is now running.")
    while True:
        command = take_command()
        if command != "none":
            process_command(command)
