from datetime import datetime
from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import wikipedia as wiki
import os

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
    
    trainnot()

def wikipedia():

    talk("What do you want me to search")

    query = listen()
    
    print (query)

    try:        
        talk (f"According to wikipedia {query} is")
        result = wiki.summary(query, sentences=3)
    except wiki.exceptions.PageError:
        talk(f"Page for {query} doesnt exist")
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

def name():
    talk("My name is jarvis the voice assistant, and you are?")
    name = listen()
    talk(f"I am pleased to bo working for you{name}")

def there():
    talk ('I am always here sir. What can I do for you?')

def trainnot():
    talk("Do you want to train the model or load it?")
    choice = listen()

    if 'train' in choice:
        if os.path.exists('assistant_model.h5'):
            os.remove('assistant_model.h5')
            os.remove('assistant_model_words.pkl')
            os.remove('assistant_model_classes.pkl')
        talk ('training')
        assistant.train_model()
        assistant.save_model()
        talk ('The model is ready to use')
    
    if 'load' in choice:
        if not os.path.exists('assistant_model.h5'):
            talk ('There is no model to be loaded, training')
            assistant.train_model()
            assistant.save_model()
        assistant.load_model()
        talk ('loading')



mappings = {
    "wikipedia": wikipedia,
    "create_todo": create_todo,
    "show_todos": show_todo,
    "create_notes": create_note,
    "name": name,
    "there": there
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)


greeting()

while True:
    message = listen()
    print(message)

    if 'stop' in message:
        talk ("Goodbye, see you soon")
        exit (0)
    if 'jarvis' in message:
        message = message.replace('jarvis', '')
        assistant.request(message)