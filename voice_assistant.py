import speech_recognition as sr
import pyttsx3
from database import add_transaction

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Speech service unavailable.")
            return ""

def process_command(command):
    if "add income" in command:
        try:
            amount = float(command.split("add income")[1].strip().split()[0])
            category = " ".join(command.split("add income")[1].strip().split()[1:])
            add_transaction("Income", amount, category)
            speak(f"Income of {amount} added under {category}.")
        except:
            speak("Sorry, could not process the income command.")
    elif "add expense" in command:
        try:
            amount = float(command.split("add expense")[1].strip().split()[0])
            category = " ".join(command.split("add expense")[1].strip().split()[1:])
            add_transaction("Expense", amount, category)
            speak(f"Expense of {amount} added under {category}.")
        except:
            speak("Sorry, could not process the expense command.")
    elif "summary" in command:
        speak("Feature not yet implemented in voice. Check GUI.")
    else:
        speak("Unknown command.")
