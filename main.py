from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import sys

r = sr.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Clean my room', 'Study']

def create_notes():
    global r

    speaker.say("What to you want to write onto your note")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                note = r.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename")
                speaker.runAndWait()

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                filename = r.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say("I succesfully created a file with a name {filename}", filename)
                speaker.runAndWait()
        except sr.UnknownValueError:
            r = sr.Recognizer()
            speaker.say("Didnt quite catch that, please repeat")

def create_todo():
    global r

    speaker.say("What woudl you like to add to your todo list")
    speaker.runAndWait()

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

                speaker.say("I added {todo} to your todo list")
                speaker.runAndWait()
        except sr.UnknownValueError:
            r = sr.Recognizer()
            speaker.say("I didnt understand, please repeat")
            speaker.runAndWait()

def show_todo():
    global r

    speaker.say("Your todos are")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say("Hello, what can I do for you")
    speaker.runAndWait()

def quit():
    speaker.say("It was nice chatting with you")
    speaker.runAndWait()
    exit(1)

def thanks():
    speaker.say("You are welcome")
    speaker.runAndWait()


mappings = {
    "create_notes": create_notes,
    "add_todo": create_todo,
    "show_todos":show_todo,
    "greeting": hello,
    "goodbye": quit,
    "thanks": thanks
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
