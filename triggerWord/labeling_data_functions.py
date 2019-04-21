import IPython
import os
import scipy.io.wavfile
import scipy
import numpy as np
from pydub import AudioSegment
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from tempfile import mkdtemp
import os.path as path
import time
global Ty
Ty = 1375
global Tx
Tx = 5511 # The number of time steps input to the model from the spectrogram
global n_freq
n_freq = 101 # Number of frequencies input to the model at each time step of the spectrogram



def change_filenames(dirc): 
    names = 40
    for filename in os.listdir(dirc):
        os.rename(dirc + filename, dirc + str(names) + ".wav")
        names += 1

    
def ten_sec_backgrounds(src_dirc, dis_dirc):
    ten_sec = 10 * 1000
    names = 1
    #for each background file slice it to 10 sec
    for filenames in os.listdir(src_dirc):
        #read background file
        data = AudioSegment.from_wav(src_dirc+filenames)
        #slice data to ten sec audio files
        for i in range(int(data.duration_seconds/10)):
            temp_data = data[ten_sec*i:ten_sec*(i+1)]
            temp_data.export(dis_dirc+str(names)+".wav", format="wav")
            names += 1
            

def get_random_time_segment(segment_ms):
    """
    Gets a random time segment of duration segment_ms in a 10,000 ms audio clip.
    
    Arguments:
    segment_ms -- the duration of the audio clip in ms ("ms" stands for "milliseconds")
    
    Returns:
    segment_time -- a tuple of (segment_start, segment_end) in ms
    """
    #print("segment_ms" + str(segment_ms))
    segment_start = np.random.randint(low=0, high=10000-segment_ms)   # Make sure segment doesn't run past the 10sec background 
    segment_end = segment_start + segment_ms - 1
    #print("segment_end" + str(segment_end))

    return (segment_start, segment_end)        
    

def is_overlapping(segment_time, previous_segments):
    """
    Checks if the time of a segment overlaps with the times of existing segments.
    
    Arguments:
    segment_time -- a tuple of (segment_start, segment_end) for the new segment
    previous_segments -- a list of tuples of (segment_start, segment_end) for the existing segments
    
    Returns:
    True if the time segment overlaps with any of the existing segments, False otherwise
    """
    
    segment_start, segment_end = segment_time
    
    # Step 1: Initialize overlap as a "False" flag. (≈ 1 line)
    overlap = False
    
    # Step 2: loop over the previous_segments start and end times.
    # Compare start/end times and set the flag to True if there is an overlap (≈ 3 lines)
    for previous_start, previous_end in previous_segments:
        if segment_start <= previous_end and segment_end >= previous_start:
            overlap = True


    return overlap

def insert_audio_clip(background, audio_clip, previous_segments):
    """
    Insert a new audio segment over the background noise at a random time step, ensuring that the 
    audio segment does not overlap with existing segments.
    
    Arguments:
    background -- a 10 second background audio recording.  
    audio_clip -- the audio clip to be inserted/overlaid. 
    previous_segments -- times where audio segments have already been placed
    
    Returns:
    new_background -- the updated background audio
    """
    
    
    
    # Get the duration of the audio clip in ms
    segment_ms = len(audio_clip)
    
    ### START CODE HERE ### 
    # Step 1: Use one of the helper functions to pick a random time segment onto which to insert 
    # the new audio clip. (≈ 1 line)
    segment_time = get_random_time_segment(segment_ms)
    
    # Step 2: Check if the new segment_time overlaps with one of the previous_segments. If so, keep 
    # picking new segment_time at random until it doesn't overlap. (≈ 2 lines)
    while is_overlapping(segment_time, previous_segments):
        segment_time = get_random_time_segment(segment_ms)
        
    # Step 3: Add the new segment_time to the list of previous_segments (≈ 1 line)
    previous_segments.append(segment_time)
    ### END CODE HERE ###
    
    # Step 4: Superpose audio segment and background
    new_background = background.overlay(audio_clip, position = segment_time[0])
    
    return new_background, segment_time

def insert_ones(y, segment_end_ms):
    """
    Update the label vector y. The labels of the 50 output steps strictly after the end of the segment 
    should be set to 1. By strictly we mean that the label of segment_end_y should be 0 while, the
    50 followinf labels should be ones.
    
    
    Arguments:
    y -- numpy array of shape (1, Ty), the labels of the training example
    segment_end_ms -- the end time of the segment in ms
    
    Returns:
    y -- updated labels
    """
    k = 10000.0
    # duration of the background (in terms of spectrogram time-steps)
    segment_end_y = int(segment_end_ms * Ty / 10000.0)
    #print(segment_end_y)
    # Add 1 to the correct index in the background label (y)
    ### START CODE HERE ### (≈ 3 lines)
    
    for k in range(segment_end_y + 1,segment_end_y + 51):        
        y[0, k] = 1.0
       

    ### END CODE HERE ###
    
    #print(y[0,:100])
    #print(y[0,-100:])    
    #plt.plot(y[0,:])
    #plt.show()
    return y



def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def load_raw_audio(backgrounds_dirc, postives_dirc, negatives_dirc):
    
    #define backgrounds, postives and negatives arrays
    backgrounds, postives, negatives = [], [], [],
    
    #for all backgrounds files
    for background_name in os.listdir(backgrounds_dirc):
        try:
            background = AudioSegment.from_wav(backgrounds_dirc + background_name)
            backgrounds.append(background)
            
        except Exception as e:
            print("file " + backgrounds_dirc + background_name + " is corrupted!")
            
    
    #for all postives files
    for postive_name in os.listdir(postives_dirc):
        try:
            postive = AudioSegment.from_wav(postives_dirc + postive_name)
            postives.append(postive)
            
        except Exception as e:
            print("file " + postives_dirc + postive_name + " is corrupted!")
        
   
    #for all negatives files
    for negative_name in os.listdir(negatives_dirc):
        try:
            negative = AudioSegment.from_wav(negatives_dirc + negative_name)
            negatives.append(negative)
        except Exception as e:
            print("file " + negatives_dirc + negative_name + " is corrupted!")

    
    return backgrounds,postives,negatives

def graph_spectrogram(file):
    
    rate, data = scipy.io.wavfile.read(file)
    nfft = 200 # Length of each window segment
    fs = 8000 # Sampling frequencies
    noverlap = 120 # Overlap between windows
    nchannels = data.ndim
    if nchannels == 1:
        pxx, freqs, bins, im = plt.specgram(data, nfft, fs, noverlap = noverlap)
    elif nchannels == 2:
        pxx, freqs, bins, im = plt.specgram(data[:,0], nfft, fs, noverlap = noverlap)
    plt.show()
    return pxx

def get_spectrogram(data):
    """
    Function to compute a spectrogram.
    
    Argument:
    predictions -- one channel / dual channel audio data as numpy array

    Returns:
    pxx -- spectrogram, 2-D array, columns are the periodograms of successive segments.
    """
    nfft = 200 # Length of each window segment
    fs = 8000 # Sampling frequencies
    noverlap = 120 # Overlap between windows
    nchannels = data.ndim
    if nchannels == 1:
        pxx, _, _ = mlab.specgram(data, nfft, fs, noverlap = noverlap)
    elif nchannels == 2:
        pxx, _, _ = mlab.specgram(data[:,0], nfft, fs, noverlap = noverlap)
    return pxx

def create_training_example(background, activates, negatives, background_name, background_dirc):
    """
    Creates a training example with a given background, activates, and negatives.
    
    Arguments:
    background -- a 10 second background audio recording
    activates -- a list of audio segments of the word "activate"
    negatives -- a list of audio segments of random words that are not "activate"
    
    Returns:
    x -- the spectrogram of the training example
    y -- the label at each time step of the spectrogram
    """

    # Set the random seed
    np.random.seed()
   
    # Make background quieter
    background = background - 20
    
    ### START CODE HERE ###
    # Step 1: Initialize y (label vector) of zeros (≈ 1 line)
    y = np.zeros((1, Ty))

    # Step 2: Initialize segment times as empty list (≈ 1 line)
    previous_segments = []
    ### END CODE HERE ###
    
    # Select 0-4 random "activate" audio clips from the entire list of "activates" recordings
    number_of_activates = np.random.randint(0, 5)
    random_indices = np.random.randint(len(activates), size=number_of_activates)
    random_activates = [activates[i] for i in random_indices]
    
    ### START CODE HERE ### (≈ 3 lines)
    # Step 3: Loop over randomly selected "activate" clips and insert in background
    #print("random_activates" + str(random_indices.reshape(random_indices.shape[0],1)[:,0]))
    for random_activate in random_activates:
        # Insert the audio clip on the background
        background, segment_time = insert_audio_clip(background, random_activate, previous_segments)
        #print("noInsert" + str(noInsert))

        # Retrieve segment_start and segment_end from segment_time
        segment_start, segment_end = segment_time
        # Insert labels in "y"
        y = insert_ones(y, segment_end)
        #plt.plot(y[0,:])
        #plt.show()
   

    # Select 0-2 random negatives audio recordings from the entire list of "negatives" recordings
    number_of_negatives = np.random.randint(0, 3)
    random_indices = np.random.randint(len(negatives), size=number_of_negatives)
    random_negatives = [negatives[i] for i in random_indices]

    ### START CODE HERE ### (≈ 2 lines)
    # Step 4: Loop over randomly selected negative clips and insert in background
    for random_negative in random_negatives:
        # Insert the audio clip on the background
        background, _, _ = insert_audio_clip(background, random_negative, previous_segments)
    ### END CODE HERE ###
    
    # Standardize the volume of the audio clip 
    background = match_target_amplitude(background, -20.0)

    # Export new training example 
    file_handle = background.export(background_dirc + background_name + ".wav", format="wav")
    print("File (" + background_name + ".wav) was saved in " + background_dirc)
    
    # Get and plot spectrogram of the new recording (background with superposition of positive and negatives)
    x = graph_spectrogram(background_dirc + background_name + ".wav")
    
    return x, y

def training_examples(n):
    backgrounds = os.listdir("./raw-audio/backgrounds/")
    global m
    m = int(len(backgrounds)) * n
    return m

def create_training_data(backgrounds, postives, negatives, train_audio_dirc, train_data_dirc):

   
    filename_x = "newfile_x.dat"
    filename_y = "newfile_y.dat"

    training_examples(5)

    batch = int(m/5)

    print("batch_size:" + str(batch))

    file_number=0
    for s in range(5):
        #create X training set
        X = np.memmap(filename_x, dtype = "float64", mode = "w+", shape = (batch, Tx, n_freq))
        #itr = 0;
        #create Y training set
        Y = np.memmap(filename_y, dtype = "float64", mode = "w+", shape = (batch, Ty, 1))
        i=0   
        #for all the backgrounds
        for i in range(len(backgrounds)):
        
            x, y = create_training_example(backgrounds[i], postives, negatives, str(file_number+1), train_audio_dirc)

            X[i,:,:], Y[i,:,:] = x.swapaxes(0,1), y.swapaxes(0,1)

            #print("................")
            #if( i == len(backgrounds)):
                #i = 0;
                #itr += 1
            #if(itr == 5):
                #break;
            file_number += 1

        print("Saving training sets....")
        #save training X data set
        np.save(train_data_dirc + "X_" + str(s + 1) + ".npy", X);
        print("training data 'X_" + str(s + 1) +"' were saved in " + train_data_dirc)

        #save training Y data set
        np.save(train_data_dirc + "Y_" + str(s+1) + ".npy", Y);
        print("training data 'Y_" + str(s+1) + "' were saved in " + train_data_dirc)
    
        print("each 'X' traing example has " + str(X[0,:,:].shape) + " shape.")
        print("each 'Y' traing example has " + str(Y[0,:,:].shape) + " shape.")

        del X
        del Y
                 
                
    
def split_training_data():

    m = training_examples(5)
    X = np.memmap("./XY_train/X.npy", dtype="float64", mode='r', shape = (m - 5, Tx, n_freq))
    Y = np.memmap("./XY_train/Y.npy", dtype="float64", mode='r', shape = (m - 5, Ty, 1))
    b = 0;
    batch = int(m / 5)
    print("batch size: " + str(batch))
    for i in range(5):
        if(i == 4):
            b = -5
        np.save("./XY_train/" + "X_" + str(i + 1) + ".npy", X[batch * i:batch * (i + 1) + b,:,:])
        print("training data 'X_" + str(i+1) +"' were saved in " +  "./XY_train/")   
        np.save("./XY_train/" + "Y_" + str(i + 1) + ".npy", Y[batch * i:batch * (i + 1) + b,:,:])
        print("training data 'Y_" + str(i+1) +"' were saved in " +  "./XY_train/")
        
        
    
    

