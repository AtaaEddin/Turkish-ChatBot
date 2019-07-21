

# Interactive ChatBot in Turkish




<p align="center">
<b>Query: sen güzel bir kızsın. </b><br>
<b>ChatBot: sen daha güzelsin!!</b><br><br>
<img width="600" src="https://media.giphy.com/media/1r8YRUc7Y7BwoaCC42/giphy.gif"/> 
</p>

we trained seq2seq model on Turkish twitter data to build a chatbot, and we built an interface(human head) to intract with the chatbot.

## Prerequisites
- python3
- [TensorFlow](https://github.com/tensorflow/tensorflow) <= 1.11.0
- [TensorLayer](https://github.com/zsdonghao/tensorlayer) >= 1.6.3
- in addition you have to be connected to internet 

## How it works

This repository  contains two main parts, trigger word part (triggerWord folder) and chatbot part (chatbot folder)


- **Trigger Word Detection**

Here is come the first part the trigger word part!
In order to interacte with human interface and speak with it! you have to wake it up.

	**Uyan Ay** ===> 
	
	<img src="https://media.giphy.com/media/TakZY1jvx5ThjAuk4m/giphy.gif"/></a>

	

	we trained our bot to wake up whenever it hears 'uyan ay', it is similar to amazon Alex when it hears 'Alex' trigger word, it wakes up.

- **ChatBot**

	our bot is task-specfic chatbot it has one task called general conversation, what it does is for any query text given to it (ex: question, jokes, ..) it repoenses with other text(answer,make statement), derived and similir to twitter responses.

	first your voice will be converted to text using voice recognition api from google, then feeded to the text-to-text AI system finally the result will be printed to the human interface(as voice and text). 

	***query: seni çok seviyorum.***
	
	***ChatBot: ben de seni çok seviyorum yanımızda olduğun için sonsuz teşekkürler.***
	
	<img algin="center" src="https://media.giphy.com/media/7XrDb6fGsWoKy9DWrb/giphy.gif" title="made at imgflip.com"/></a>

## Instalation

- **ubuntu**

	if you are on ubuntu you should run first:     
	```sh
	$ sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools

	$ sudo apt-get install python3-tk 
	```
	after that run this:

		- Ubuntu python3:
			pip3 install -r requirements.txt

		- Ubuntu python:
			pip install -r requirements.txt

- **windows**

	I didn't test it on windows but it should be working fine.

		run: pip install -r requirements.txt

## run the chatbot
	Ubuntu:
		for python 3: 
			python3 my_robot.py
		for python 2:
			python my_robot.py

	Windows:
		python my_robot.py

