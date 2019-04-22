

# Interactive ChatBot in Turkish




<p align="center">
<b>Query: sen güzel bir kızsın. </b><br>
<b>ChatBot: sen daha güzelsin!!</b><br><br>
<img width="600" src="https://media.giphy.com/media/1r8YRUc7Y7BwoaCC42/giphy.gif"/> 
</p>

we trained seq2seq model on Turkish twitter data to build a chatbot, and we wrapped our chatbot with human talking head, and above that we trained other model to detect trigger word as start point to chat and open conversation with the chatbot.  

## Prerequisites
- python3
- [TensorFlow](https://github.com/tensorflow/tensorflow) <= 1.11.0
- [TensorLayer](https://github.com/zsdonghao/tensorlayer) >= 1.6.3
- in addition you have to be connected to internet 

## How it works

This repository  contains to main parts, trigger word part (triggerWord folder) and chatbot part (chatbot folder)

In order to interacte with the chatbot first you have to wake it up.

- **Trigger Word Detection**

	**Uyan Ay** ===> 
	
	<img src="https://media.giphy.com/media/TakZY1jvx5ThjAuk4m/giphy.gif"/></a>

	Here is come the first part the trigger word part!

	we trained our bot to wake up whenever it hears 'uyan ay', it is similar to amazon Alex when it hears 'Alex' trigger word, it wakes up.

- **ChatBot**

	our bot is task-specfic chatbot it has one task called general conversation, what it does is respones to any query text given to it (ex: question, jokes, ..) with other meaningful text hopefuly :), derived and similir to twitter responses.

	Instead of writting to the chatbot we add the voice recognition api serves from google, so your speech will be converted automatically to text and fed to the chatbot.

	***query: seni çok seviyorum.***
	***ChatBot: ben de seni çok seviyorum yanımızda olduğun için sonsuz teşekkürler.***
	<img algin="center" src="https://media.giphy.com/media/7XrDb6fGsWoKy9DWrb/giphy.gif" title="made at imgflip.com"/></a>

## Instalation

- **ubuntu**

	if you are on ubuntu you should run first:     

		sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools

		sudo apt-get install python3-tk 

	after that run this:

		- Ubuntu python3:
			pip3 install -r requirements.txt

		- Ubuntu python:
			pip install -r requirements.txt

- **windows**

	I didn't test it on windows but it should work fine.

		run: pip install -r requirements.txt

## run the chatbot
	Ubuntu:
		for python 3: 
			python3 my_robot.py
		for python 2:
			python my_robot.py

	Windows:
		python my_robot.py
