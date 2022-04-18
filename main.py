from datetime import datetime
from sre_constants import SUCCESS
from neuralintents import GenericAssistant
from requests import delete
import speech_recognition as sr
import pyttsx3 as tts
import wikipedia as wiki
import os
import python_weather

    # TODO
    #    1. Wether look
    #    2. Reminders
    #    3. Calculations

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
       

def hello():
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

    try:        
        talk (f"According to wikipedia {query} is")
        result = wiki.summary(query, sentences=3)
    except wiki.exceptions.PageError:
        talk(f"Page for {query} doesnt exist")
    except wiki.exceptions.DisambiguationError:
        talk("There are too many results, try again")
    talk(result)

async def weather():
    client = python_weather.Client(format=python_weather.METRIC)

    weather = await client.find("Ljubljana")

    print(weather.current.temperature)
    talk(weather.current.temperature)
    
    talk('Forcast for upocomming days is')

    for forecast in weather.forecasts:
        print(str(forecast.date), forecast.sky_text, forecast.temperature)
        talk(str(forecast.date), forecast.sky_text, forecast.temperature)

    await client.close()




def create_todo():

    talk ("What would you like to add to your todo list")

    todo = listen()

    todo_list.append(todo)

    talk (f"I added {todo} to your todos")
    print (f"{todo}")

def show_todo():
    for item in todo_list:
        talk (item)

def remove_todo():
    talk("What should I remove from your todo list")

    item = listen()

    if 'item' in todo_list:
        todo_list.remove(item)
    
    talk (f"I removed {item} from yout todo list")

def create_note():
    talk ("What would you like to write to your notes")
    note = listen()

    talk ("Choose a filename")
    filename = listen()

    with open(os.path.join("scripts/notes", filename), 'w') as f:
        f.write(note)
    talk (f"Succesfully created a note with a name {filename}")

def delete_note():
    talk ("What note would you like to delete?")

    try:
        item = listen()

        if os.path.exists(os.path.join("scripts\notes",item)):
            os.remove(item)
            talk (f"I removed {item} from your notes")
        else:
            talk(f"{item} filename doesnt exist, retrying")
    except SUCCESS:
        return

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
        talk ('loading')
        if not os.path.exists('assistant_model.h5'):
            talk ('There is no model to be loaded, training')
            assistant.train_model()
            assistant.save_model()
        assistant.load_model()
        talk ('The model was loaded')



mappings = {
    "wikipedia": wikipedia,
    "create_todo": create_todo,
    "delete_todo": remove_todo,
    "show_todos": show_todo,
    "create_notes": create_note,
    "delete_note": delete_note,
    "name": name,
    "there": there,
    "hello":hello,
    "weather": weather
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)


hello()
trainnot()

while True:
    message = listen()
    print(message)

    if 'stop' in message:
        talk ("Goodbye, see you soon")
        exit (0)
    assistant.request(message)