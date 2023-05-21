#Invocación de librerías

import os
from llama_cpp import Llama
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from playsound import playsound
import json
import time
from flask import Flask, redirect, url_for, render_template, request, redirect, session
import subprocess
import requests
from requests.structures import CaseInsensitiveDict

ubicacion='/home/luis/chat/static'

app=Flask(__name__)
app.secret_key = '007'

@app.route("/")
def main():
   return render_template("/login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Add your authentication logic here
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect('/chat')
        else:
            return render_template('login.html', error='Invalid username or password')
   else:
      return render_template('login.html')
   
   


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        
        # Get the audio data from the request
        audio_data = request.files['audio']
        audio_data.save(ubicacion+'/audio.wav')
        # Save the audio to a file or process it as needed
        
        #conversion de audio
        subprocess.run('python3 conver.py', shell=True)
        
        #Google audio
        r = sr.Recognizer()
        voz=sr.AudioFile(ubicacion+'/audio.flac')
        
        with voz as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            texto=r.recognize_google(audio)
            
            #Enviar request a Llama IA
            response=teacher_typing(texto)
            tts = gTTS(response, lang='en-us')
            tts.save(ubicacion+'/recived_audio.mp3')
            
        
            return 'functions sucessfully invoqued!'         

    return render_template('chat1.html')

#Logica para comunicacion con el chat
#Hasta acascript de pagina web
def teacher_typing(enunciado):
    url = "http://localhost:8000/v1/completions"

    
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    data = """
    {
     "prompt": "### Instructions: %s ### Response: ",
     "stop": [
       " n",
       "###"
    ]
    }
    """%(enunciado)
    respuesta = requests.post(url, headers=headers, data=data)
    res=respuesta.json()["choices"][0]["text"]
    return res
    

if __name__=="__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
