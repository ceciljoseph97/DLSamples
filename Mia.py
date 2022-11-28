import google.cloud.dialogflow_v2 as dF
import os
from gtts import gTTS
import pyttsx3
from pygame import mixer
from mutagen.mp3 import MP3
import time

language = 'en'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ServiceKeyJsonFromDF"
os.environ["DIALOGFLOW_PROJECT_ID"]="Project_ID"

project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
session_id="any_random_unique_string"

def detect_intent(project_id, session_id, text, language_code):

    session_client = dF.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dF.types.TextInput(text=text, language_code=language_code)
    query_input = dF.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text

exit_conditions = (":q", "quit", "exit")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #Fem_Voice
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 180)     # setting up new voice rate
flag=0
while(True):
    message = input("> ")
    if("music" in message):
        flag=1
    else:
        flag=0
    if message in exit_conditions:
        break
    else:
        fulfillment_text = detect_intent(project_id, session_id, message, 'en')
        print(f"🤖 {fulfillment_text}")
        engine.say(fulfillment_text)
        engine.runAndWait()
        if(flag==1 and "Adele" in fulfillment_text):
            try:
                mixer.init()
                mixer.music.load('AdeleHello.mp3')
                mixer.music.play()
                audio = MP3("AdeleHello.mp3")
                time.sleep(audio.info.length)
            except KeyboardInterrupt:
                mixer.music.stop()