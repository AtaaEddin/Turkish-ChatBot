import speech_recognition as sr
from gtts import gTTS
#import winsound
import os
#quiet the endless 'insecurerequest' warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
from pygame import mixer
mixer.init()
 
#from mpg123 import Mpg123, Out123



# use libout123 to access the sound device
#out = Out123()

def listen(nope):
  # obtain audio from the microphone
  r = sr.Recognizer()
  with sr.Microphone() as source:
    #print("Please wait. Calibrating microphone...")
    # listen for 1 second and create the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say something!")
    audio = r.listen(source,phrase_time_limit=5)
 
  # recognize speech using Sphinx/Google
  try:
    #response = r.recognize_sphinx(audio)
    response = r.recognize_google(audio, language="tr")
    f = open("query.txt", "w", encoding='utf-8')
    f.write(str(response))

    print("I think you said '" + response + "'")

    #tts = gTTS(text= str(response), lang='tr')
    #tts.save("response.mp3")

    #mixer.music.load('response.mp3')
    #mixer.music.play()
    
    #winsound.PlaySound('E:\\my projects\\voice_recognition\\response.wav', winsound.SND_FILENAME)

    # load an mp3 file
    #mp3 = Mpg123('response.mp3')

    # decode mp3 frames and send them to the sound device
    #for frame in mp3.iter_frames(out.start):
      #out.play(frame)

    #mixer.music.load('E:\\my projects\\voice_recognition\\response.mp3') # you may use .mp3 but support is limited
    #mixer.music.play()


    #os.system('mpg123 -q E:\\my projects\\voice_recognition\\response.mp3')
 
  except sr.UnknownValueError:
    print("Sphinx could not understand audio")
    open("query.txt", "w", encoding='utf-8')
  except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
    open("query.txt", "w", encoding='utf-8')

