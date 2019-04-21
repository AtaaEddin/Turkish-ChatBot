from pydub import AudioSegment
import numpy as np
from keras.models import load_model
import IPython

model =load_model("./triggerWord/model/model_v5_90.h5")
model._make_predict_function()

def trimAudio(src_dirc, dis_dirc):
    ten_sec = 10 * 1000
    names = 1
    
    #read background file
    data = AudioSegment.from_wav(src_dirc)
    #slice data to ten sec audio files
    
    temp_data = data[:ten_sec]
    temp_data.export(dis_dirc, format="wav")
            

def detect_triggerword(x):
    #plt.subplot(2, 1, 1)

    
    # the spectogram outputs (freqs, Tx) and we want (Tx, freqs) to input into the model
    x  = x.swapaxes(0,1)
    x = np.expand_dims(x, axis=0)
    
    predictions = model.predict(x)
    
    #plt.subplot(2, 1, 2)
    #plt.plot(predictions[0,:,0])
    #plt.ylabel('probability')
    #plt.show()

    #inflatte predections 
    return predictions.reshape(-1)

def has_new_triggerword(predictions, chunk_duration, feed_duration, threshold=0.7):
    """
    Function to detect new trigger word in the latest chunk of input audio.
    It is looking for the rising edge of the predictions data belongs to the
    last/latest chunk.
    
    Argument:
    predictions -- predicted labels from model
    chunk_duration -- time in second of a chunk
    feed_duration -- time in second of the input to model
    threshold -- threshold for probability above a certain to be considered positive

    Returns:
    True if new trigger word detected in the latest chunk
    """
    """
    predictions = predictions > threshold
    chunk_predictions_samples = int(len(predictions) * chunk_duration / feed_duration)
    chunk_predictions = predictions[-chunk_predictions_samples:]
    
    #level = chunk_predictions[0]
    #for pred in chunk_predictions:
    #    if pred > level:
    #        return True
    #    else:
    #        level = pred
    #return False
    """

    chunk_predictions_samples = int(len(predictions) * (chunk_duration) / feed_duration)
    predictions = predictions[-chunk_predictions_samples:]

    counter = 0
    for pred in predictions:
        if pred > threshold: 
            counter += 1
        if counter > 40:
            print(counter, end='')
            return True
    print(counter, end='')            
    return False

    
"""
chime_file = "./chime.wav"

def chime_on_activate(filename, predictions, threshold):
    audio_clip = AudioSegment.from_wav(filename)
    chime = AudioSegment.from_wav(chime_file)
    Ty = predictions.shape[1]
    # Step 1: Initialize the number of consecutive output steps to 0
    consecutive_timesteps = 0
    # Step 2: Loop over the output steps in the y
    for i in range(Ty):
        # Step 3: Increment consecutive output steps
        consecutive_timesteps += 1
        #print(predictions[0,i,0])
        # Step 4: If prediction is higher than the threshold and more than 75 consecutive output steps have passed
        print(predictions[0,i,0])
        if predictions[0,i,0] > threshold and consecutive_timesteps > 100:
            # Step 5: Superpose audio and background using pydub
            audio_clip = audio_clip.overlay(chime, position = ((i / Ty) * audio_clip.duration_seconds)*1000)
            # Step 6: Reset consecutive output steps to 0
            consecutive_timesteps = 0
            print("lol")
        
    audio_clip.export("chime_output.wav", format='wav')


trimAudio("example.wav","example_tenSec.wav")

filename = "example_tenSec.wav"
prediction = detect_triggerword(filename)
chime_on_activate(filename, prediction, 0.8)


"""