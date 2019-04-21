from keras.callbacks import ModelCheckpoint
from keras.models import Model, load_model, Sequential
from keras.layers import Dense, Activation, Dropout, Input, Masking, TimeDistributed, LSTM, Conv1D
from keras.layers import GRU, Bidirectional, BatchNormalization, Reshape
from keras.optimizers import Adam

def model(input_shape):
    
    """
    unction creating the model's graph in Keras.
    
    Argument:
    input_shape -- shape of the model's input data (using Keras conventions)

    Returns:
    model -- Keras model instance
    """

    X_input = Input(shape=input_shape)

    #setp 1: CONV layer
    X = Conv1D(filters = 196, kernel_size = 15, strides = 4)(X_input)
    X = BatchNormalization(axis = -1)(X)
    X = Activation("relu")(X)
    X = Dropout(0.8)(X)

    #setp 2: First GRU layer
    X = GRU(units = 128, return_sequences = True)(X)
    X = Dropout(0.8)(X)
    X = BatchNormalization(axis = -1)(X)

    #setp 3: Secnod GRU layer
    X = GRU(units = 128, return_sequences = True)(X)
    X = Dropout(0.8)(X)
    X = BatchNormalization(axis = -1)(X)
    X = Dropout(0.8)(X)

    #setp 4: TimeDistributed dense layer
    X = TimeDistributed(Dense(1, activation = "sigmoid"))(X)

    model = Model(inputs = X_input, outputs = X)

    return model
    
    
