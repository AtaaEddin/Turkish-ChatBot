from labeling_data_functions import *
#from rnn_model import *
import matplotlib.pyplot as plt
#from keras.models import load_model

#change_filenames("./poses/")
##Y = np.load("./XY_train/Y.npy")
##plt.plot(Y[1,:,0])
##
##plt.show()

#X = graph_spectrogram("./audio for training/6.wav")
"""
m = training_examples(5)


#split_training_data()

##X_1 = np.load("./XY_train/Y_1.npy")
##plt.plot(X_1[0,:,0])
##plt.show()        
X = np.memmap("./XY_train/Y_1.npy", dtype="float64", shape=(715,Ty,1))
Y = np.memmap("./XY_train/X_1.npy", dtype="float64", shape=(715,Ty,1))
#print(X[0,:100,0])
for i in range(700):
    print(i)
    print(X[i,:100,0])
    print(X[i,-100:,0])
    plt.plot(X[i,:,0])
    plt.show()
"""

"""
for i in range(5):
    X = np.load("./XY_train/X_" + str(i+1) + ".npy")
    print(str(X.shape))
    Y = np.load("./XY_train/Y_" + str(i+1) + ".npy")
    print(str(Y.shape))
"""
"""
model_dirc = "./model/"
epoch_num = 50
model = model(input_shape = (Tx, n_freq))
opt = Adam(lr = 0.0001, beta_1 = 0.9, beta_2 = 0.999, decay = 0.01)
model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics=["accuracy"])
for j in range(epoch_num):
    print("............................")
    print("epoch" + str(j+1) + "/" + str(epoch_num))
    print("............................")
    for i in range(5):    
        X = np.load("./XY_train/X_" + str(i+1) + ".npy")
        Y = np.load("./XY_train/Y_" + str(i+1) + ".npy")
        model.fit(X, Y, batch_size = 64, epochs = 1)
        

#model.summery()


model.save(model_dirc + "model_v2.h5")

"""
"""
print("loool")


backgrounds_dirc = "./raw-audio/backgrounds/"
postives_dirc = "./raw-audio/wav postive/"
negatives_dirc = "./raw-audio/wav negatives/"
train_audio_dirc = "./audio for training/"
if not os.path.exists(train_audio_dirc):
    os.makedirs(train_audio_dirc)
train_data_dirc = "./XY_train/"
if not os.path.exists(train_data_dirc):
    os.makedirs(train_data_dirc)

#change_filenames("./raw audio/wav postive/")


backgrounds,postives,negatives = load_raw_audio(backgrounds_dirc,postives_dirc,negatives_dirc)


#print(np.array(backgrounds).shape)
#print(np.array(postives).shape)
#print(len(negatives[0]))

create_training_data(backgrounds, postives, negatives, train_audio_dirc, train_data_dirc)

model_dirc = "./model/"
epoch_num = 100
#model = model(input_shape = (Tx, n_freq))
model = load_model("./model/model_v2.h5")
opt = Adam(lr = 0.0001, beta_1 = 0.9, beta_2 = 0.999, decay = 0.01)
model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics=["accuracy"])
for j in range(epoch_num):
    print("............................")
    print("epoch" + str(j+1) + "/" + str(epoch_num))
    print("............................")
    for i in range(5):    
        X = np.load("./XY_train/X_" + str(i+1) + ".npy")
        Y = np.load("./XY_train/Y_" + str(i+1) + ".npy")
        model.fit(X, Y, batch_size = 128, epochs = 1)

        if j % 50 == 0:
            model.save(model_dirc + "model_v3_" + str(j) + ".h5")
        .

model.save(model_dirc + "model_v3.h5")
"""
graph_spectrogram("E:/my projects/bigbug/audio for training/6.wav")
