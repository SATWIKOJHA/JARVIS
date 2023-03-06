import speech_recognition as sr
import spacy
import pyttsx3
import os

# Initialize the speech recognition engine
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Initialize the natural language processing pipeline
nlp = spacy.load("en_core_web_sm")

# Define the command and control logic
def process_command(command):
    doc = nlp(command)
    intent = doc[0].lemma_
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    if intent == "greet":
        engine.say("Hello, how can I help you?")
        engine.runAndWait()
    elif intent == "search":
        engine.say("Searching for " + entities[0][0])
        engine.runAndWait()
        # Code to perform the search
    elif intent == "play":
        if entities[0][1] == "song":
            song_name = entities[0][0]
            engine.say("Playing " + song_name)
            engine.runAndWait()
            os.system("open -a QuickTime\ Player /path/to/music/folder/" + song_name + ".mp3")

# Record the audio from the user
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# Recognize the speech and process the command
try:
    text = r.recognize_google(audio)
    process_command(text)
except sr.UnknownValueError:
    print("Sorry, I could not understand what you said")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
