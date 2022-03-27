from email import message
import speech_recognition as sr
from neuralintents import GenericAssistant as ga
import pyttsx3 as tts
import sys

r = sr.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = {'Add note'}

def create_note():
    global recognizer

    speaker.say("What do you want me to add to your notes")
    speaker.runAndWait()

    done = False

    while not done:

        try:

            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                note = r.recognize_google(audio)

                note = note.lower()

                speaker.say ("Choose a filename")
                speaker.runAndWait()

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                filename = r.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
            
                f.write(note)
                speaker.say ("I made a note {filename}")
                speaker.runAndWait

        except sr.UnknownValueError:
            r = sr.Recognizer()
            speaker.say("Didnt recognzie, please try again")
            speaker.runAndWait()

mappings = {'note': create_note}

assistant = ga('intents.json', intent_methods=mappings)
assistant.train_model()

while True:

    try:
        with sr.Microphone() as mic:

            r.adjust_for_ambient_noise(mic, duration=0.2)
            audio = r.listen(mic)

            message = r.recognize_google(audio)
            message = message.lower()

        assistant.request(message)

    except sr.UnknownValueError:
        r = sr.Recognizer()

