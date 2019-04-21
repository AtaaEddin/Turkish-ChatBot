import pygame, sys, time, random
from pygame.locals import *
from time import *
import curses
#from curses.ascii import isdigit

import os
import _thread
import threading
import re
import triggerWord.trigger_word_from_audio_stream
from triggerWord.trigger_word_from_audio_stream import detect
from triggerWord.trigger_word_from_audio_stream import initDetecter
import queue
from voiceRecognition import listen
from gtts import gTTS
from pygame import mixer
from chatbot import main_simple_seq2seq
from chatbot.main_simple_seq2seq import predict
import shutil
import time
import pydub

mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

input_q = queue.Queue()
result_q = queue.Queue()

#init things...
pygame.init()
windowSurface = pygame.display.set_mode((390, 510), 0, 32)
pygame.display.set_caption("Bounce")

pygame.event.get()
	
info = pygame.display.Info()
sw = info.current_w
sh = info.current_h
y = 0
windowSurface.fill(WHITE)
myfont = pygame.font.SysFont("ComicSans", 35)

def load_all_imgs(directory):
	return {str(f): pygame.image.load(directory + f) for f in os.listdir(directory)} 

imgsMapper = load_all_imgs("./chatbot_imags/")

#graphic function
def sleeping():

	displayImg(imgsMapper['sleeping.jpg'])
	windowSurface.fill(BLACK)

	
def getAnswer(query):
	answers = []
	#random.seed(10)
	answers = predict(query)
	
	answers = [" ".join(answer.split()) for answer in answers if not 'unk' in answer]
	#index = random.randint(0, len(answers))
	if answers == []:
		answers.append("bilmiyorum")

	f = open("getAnswer.txt", 'w', encoding = 'utf-8')
	f.write(answers[0])
	f.close() 



#graphic function
def listening():
	displayImg(imgsMapper['ready.jpg'])
	windowSurface.fill(BLACK)
	

def saySomething(answer, num):
	sound = pydub.AudioSegment.from_mp3("temp/response"+ str(num) + ".mp3")
	sound.export("temp/response"+ str(num) + ".wav",format='wav')
	mixer.music.load("temp/response"+ str(num) + ".wav")
	mixer.music.play()


def speaking(sentence, num):
	
	tts = gTTS(text= str(sentence), lang='tr')
	tts.save("temp/response"+ str(num) + ".mp3")
	#sf = TemporaryFile()
	#tts.write_to_fp("temp/response"+ str(num) + ".mp3")
	try:
		_thread.start_new_thread( saySomething,(sentence, num,))
	except Exception as e:
		print(e)
	workingSentence = " "
	sleep(0.24)
	for word in sentence.split():
		word = word.lower()
		
		timePerChar = 0.244/float(len(word))
		i = 0
		for char in word:
			if i == 0:
				displayImg(imgsMapper['ready.jpg'])
			elif i == 1:
				displayImg(imgsMapper['speaking_1.jpg'])
			elif i == 2:
				displayImg(imgsMapper['speaking_2.jpg'])
			elif i == 3:
				displayImg(imgsMapper['speaking_1.jpg'])
			else:
				i = 0

			i += 1
			myfont = pygame.font.SysFont("ComicSans", 17)
			workingSentence += char[0]
			label = myfont.render(workingSentence, 1, WHITE)
			windowSurface.blit(label, (5, 5))
			pygame.display.update()
			sleep(timePerChar + 0.1)
		workingSentence += " "
		displayImg(imgsMapper['ready.jpg'])
		myfont = pygame.font.SysFont("ComicSans", 17)
		label = myfont.render(workingSentence, 1, BLACK)
		windowSurface.blit(label, (5, 5))
		pygame.display.update()
		sleep(0.04)
	windowSurface.fill(BLACK)

	myfont = pygame.font.SysFont("ComicSans", 17)
	label = myfont.render(workingSentence, 1, BLACK)
	
	windowSurface.blit(imgsMapper['ready.jpg'],(0,0))
	windowSurface.blit(label, (5, 5))
	pygame.display.update()
	sleep(0.4)

def wakingUp():
	displayImg(imgsMapper['wakingUp_1.jpg'])
	sleep(0.1)
	displayImg(imgsMapper['wakingUp_2.jpg'])
	sleep(0.1)
	displayImg(imgsMapper['wakingUp_3.jpg'])
	sleep(0.1)
	

def displayImg(img):
	global windowSurface	
	
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	windowSurface.fill(BLACK)
	windowSurface.blit(img, (0,0))    
	pygame.display.update()
	pygame.display.flip()
	
		

def main():
	
	if os.path.exists("triggered.txt"):
		os.remove("triggered.txt")

	if not os.path.exists("temp"):
		os.makedirs("temp")

	_thread.start_new_thread(detect, (1,))
	#isinstance(result_q.get(), bool) and result_q.get() != 
	while(not os.path.exists("triggered.txt")):
		sleeping()

	wakingUp()
	random.seed(time.time())
	i = random.randint(0, 20000)
	run = True
	while run:
		
		try:
			if os.path.exists("query.txt"):
				os.remove("query.txt")

			if os.path.exists("getAnswer.txt"):
				os.remove("getAnswer.txt")

			_thread.start_new_thread(listen, (1,))

			while(not os.path.exists("query.txt")):
				listening()

			query = open("query.txt", "r", encoding = 'utf-8').read()

			#get predictions and save it to a file
			_thread.start_new_thread(getAnswer, (query,))

			while not os.path.exists("getAnswer.txt"):
				listening()

			answer = open("./getAnswer.txt", "r", encoding = 'utf-8').read()
			print(answer)
			i = random.randint(0, 20000)
			try:
				speaking(answer, i)
				
			except Exception as e:
				print(e)
			

		except (KeyboardInterrupt):
			run = False
	shutil.rmtree("./temp")
if __name__ == '__main__':
	main()

