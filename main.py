from datetime import datetime
from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import wikipedia as wiki

r = sr.Recognizer()

engine = tts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

todo_list = {"Clean my room", "Make science project"}

def talk(command):
    engine.say(command)
    engine.runAndWait()

def listen():
    global r

    done = False
    while not done:   
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                command = r.recognize_google(audio)
                command = command.lower()
                if 'alexa' in command:
                    command = command.replace('alexa ', '')
                    print (command)
                return command

        except sr.UnknownValueError:
            r = sr.Recognizer()
       

def greeting():
    hour = datetime.now().hour

    if hour >= 0 and hour <12:
        talk("Good Morning")
    elif hour >=12 and hour > 18:
        talk("Good afternoon")
    else:
        talk("Good Evening")

def wikipedia():

    talk("What do you want me to search")

    query = listen()
    
    print (query)
    if 'quit' in query:
        talk ("Quitting")
        return

    try:        
        talk (f"According to wikipedia {query} is")
        result = wiki.summary(query, sentences=3)
    except wiki.exceptions.PageError:
        talk("Page doesnt exist")
    except wiki.exceptions.DisambiguationError:
        talk("There are too many results, try again")
    talk(result)

def create_todo():

    talk ("What would you like to add to your todo list")

    todo = listen()

    todo_list.append(todo)

    talk (f"I added {todo} to your todos")
    print (f"{todo}")

def show_todo():
    for item in todo_list:
        talk (item)

def create_note():
    talk ("What would you like to write to your notes")
    note = listen()

    talk ("Choose a filename")
    filename = listen()

    with open(filename, 'w') as f:
        f.write(note)
    talk (f"Succesfully created a note with a name {filename}")

mappings = {
    "wikipedia": wikipedia,
    "create_todo": create_todo,
    "show_todos": show_todo,
    "create_notes": create_note
}

assistant = GenericAssistant('intents_better.json', intent_methods=mappings)
assistant.train_model()

greeting()

while True:
    message = listen()
    print(message)

    assistant.request(message)

