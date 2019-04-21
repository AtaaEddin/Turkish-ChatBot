import pyaudio
import pygame
from queue import Queue
from threading import Thread
import sys
import time
from triggerWord.predict import *
from triggerWord.labeling_data_functions import get_spectrogram

pygame.init()

chunk_duration = 2 # Each read length in seconds from mic.
fs = 44100 # sampling rate for mic
chunk_samples = int(fs * chunk_duration) # Each read length in number of samples.

# Each model input data duration in seconds, need to be an integer numbers of chunk_duration
feed_duration = 10
feed_samples = int(fs * feed_duration)

assert feed_duration/chunk_duration == int(feed_duration/chunk_duration)



def get_audio_input_stream(callback):
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=fs,
        input=True,
        frames_per_buffer=chunk_samples,
        input_device_index=0,
        stream_callback=callback)
    return stream


# Queue to communiate between the audio callback and main thread
q = Queue()



silence_threshold = 100



def callback(in_data, frame_count, time_info, status):
    global run, timeout, data, silence_threshold    
    if time.time() > timeout:
        run = False        
    data0 = np.frombuffer(in_data, dtype='int16')
    if np.abs(data0).mean() < silence_threshold:
        #sys.stdout.write('-')
        #print('-', end='')
        
        return (in_data, pyaudio.paContinue)
    #else:
        #sys.stdout.write('.')
        #print('.', end='')
    data = np.array(np.append(data,data0), dtype='float64')    
    if len(data) > feed_samples:
        data = data[-feed_samples:]
        # Process data async by sending a queue.
        q.put(data)
    return (in_data, pyaudio.paContinue)

def initDetecter():
    #global stream
    #stream = get_audio_input_stream(callback)
    #stream.start_stream()

    

    global run
    

    # Run the demo for a timeout seconds
    global timeout
    

    # Data buffer for the input wavform
    global data
    

def detect(nope):
    stream = get_audio_input_stream(callback)
    stream.start_stream()
    chime_file = "./triggerWord/chime.wav"
    global run, timeout, data
    
    timeout = time.time() + 0.5*60  # 0.5 minutes from now
    run = True
    data = np.zeros(feed_samples, dtype='int16')
    i = 0
    while(True == True):
        try:
            
            data = q.get()
            spectrum = get_spectrogram(data)
            preds = detect_triggerword(spectrum)
            new_trigger = has_new_triggerword(preds, chunk_duration, feed_duration)
            
            if new_trigger:
                #sys.stdout.write('1')
                #print('1', end='')
                #winsound.PlaySound(chime_file, winsound.SND_FILENAME)
                pygame.mixer.music.load(chime_file)
                pygame.mixer.music.play()
                run = False
                open("triggered.txt", "w")
                stream.stop_stream()
                stream.close()
        except (KeyboardInterrupt, SystemExit):
            stream.stop_stream()
            stream.close()
            timeout = time.time()
            run = False

    
    stream.stop_stream()
    stream.close()

    return True

