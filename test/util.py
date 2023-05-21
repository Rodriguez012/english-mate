import speech_recognition as sr
from gtts import gTTS


r = sr.Recognizer()
voz=sr.AudioFile('/home/luis/chat/static/audio.wav')

with voz as source:
   r.adjust_for_ambient_noise(source)
   audio = r.record(source)
   texto=r.recognize_google(audio)
