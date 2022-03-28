from datetime import datetime
from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import sys
import wikipedia as wiki

r = sr.Recognizer()

speaker = tts.init('sapi5')
voices=speaker.getProperty('voices')
speaker.setProperty('voice','voices[0].id')

todo_list = ['Clean my room', 'Study']

def create_notes():
    global r

    speak("What to you want to write onto your note")

    done = False

    while not done:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                note = r.recognize_google(audio)
                note = note.lower()

                speak("Choose a filename")

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                filename = r.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speak(f"I succesfully created a file with a name {filename}")

        except sr.UnknownValueError:
            r = sr.Recognizer()
            speak("Didnt quite catch that, please repeat")

def wishMe():
    hour = datetime.now().hour

    if hour >= 0 and hour <12:
        speak("Good Morning")
    elif hour >=12 and hour > 18:
        speak("Good afternoon")
    else:
        speak("Good Evening")

def wikipeida():
    global r
    speak("What would like me to search for you")

    done = False

    while not done:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                query = r.recognize_google(audio)
                query = query.lower()

                print (query)

                if query == 'exit':
                    exit(1)

                result = wiki.summary(query, sentences=3)

                speak(f"You have searched for {query}")
                speak(result)
        except sr.UnknownValueError:
            r = sr.Recognizer()
            speak("I didnt understand, please repeat")
        except wiki.exceptions.PageError:
            speak("The page doesnt exist")
        except wiki.exceptions.DisambiguationError:
            speak("There are too many result, try again")
            continue


def create_todo():
    global r

    speak("What woudl you like to add to your todo list")

    done = False

    while not done:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                todo = r.recognize_google(audio)
                todo = todo.lower()

                todo_list.append(todo)
                done = True

                speak(f"I added {todo} to your todo list")

        except sr.UnknownValueError:
            r = sr.Recognizer()
            speak("I didnt understand, please repeat")
           

def show_todo():
    global r

    speaker.say("Your todos are")
    for item in todo_list:
        speak(item)

def quit():
    speak("It was nice chatting with you")
    exit(1)

def thanks():
    speak("You are welcome")

def speak(text):
    speaker.say(text)
    speaker.runAndWait()

mappings = {
    "create_notes": create_notes,
    "add_todo": create_todo,
    "show_todos":show_todo,
    "greeting": wishMe,
    "goodbye": quit,
    "thanks": thanks,
    "wikipedia": wikipeida
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with sr.Microphone() as mic:
            r.adjust_for_ambient_noise(mic, duration=0.2)
            audio = r.listen(mic)

            message = r.recognize_google(audio)
            message = message.lower()

            print(message)

            assistant.request(message)
    except sr.UnknownValueError:
        r = sr.Recognizer()
