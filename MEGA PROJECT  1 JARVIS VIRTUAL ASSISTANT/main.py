import speech_recognition as sr

import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
# pip install pocketsphinx

recognizer = sr.Recognizer()
engine  = pyttsx3.init()
newsapi = "dbbe5ae6d6ef445190209b91c6e882c6"


def speak(text) :
    engine.say(text)
    engine.runAndWait()
    
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 
    
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()
    
    
    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
        
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    
    
    
def aiProcess(command):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

    completion = client.chat.completions.create(
   
    model="arcee-ai/trinity-large-preview:free",
    messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": command }
  ]
)

    return completion.choices[0].message.content

  

def processCommand(c) :
    if "google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open twitter" in c.lower():
        webbrowser.open("https://www.twitter.com/")
    elif c.lower().startswith("play"):
      song = c.lower().split(" ")[1]
      if song in musicLibrary.music:
        link = musicLibrary.music[song]
        webbrowser.open(link)
      else:
        speak("Song not found")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
        for article in articles:
                speak(article['title'])
        
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 



if __name__ == "__main__" :
    speak("Initializing Jarvis....")
    while True:
    
    #list for the wake word "Jarvis"
    # obtain audio from the microphone
    
      r = sr.Recognizer()
      print("recognizing...")
      try:
         with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
         word = r.recognize_google(audio)
         if "jarvis" in word.lower():
 
                speak("Ya")
            
            
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


      except Exception as e:
            print("Error; {0}".format(e))


