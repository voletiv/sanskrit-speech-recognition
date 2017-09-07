# Keras Bidirectional LSTM IMDB example - https://github.com/fchollet/keras/blob/master/examples/imdb_bidirectional_lstm.py 
# BidirectionalLSTM with masking - http://dirko.github.io/Bidirectional-LSTMs-with-Keras/
# Stateful LSTMs theory - http://philipperemy.github.io/keras-stateful-lstm/
# Seq2Seq - https://chunml.github.io/ChunML.github.io/project/Sequence-To-Sequence/
import os

from keras.models import Model, Sequential
from keras.layers import Input, Masking, LSTM, Dense, RepeatVector
from keras.layers.wrappers import Bidirectional, TimeDistributed
from keras.optimizers import Adam
from keras.preprocessing import sequence
from keras.utils import np_utils

from audio_functions import *
from devanagari_functions import *


##############################################################################
# PARAMS
##############################################################################

# Audio files
audioMFCCPath = '/home/voletiv/Datasets/BG/1/BG-C15.mp3_st.npy'
audioTimesPath = '/home/voletiv/GitHubRepos/sanskrit-speech-recognition/docs/BG-clean-C15-times.txt'
textPath = '/home/voletiv/GitHubRepos/sanskrit-speech-recognition/docs/BG-clean-C15.txt'

# MFCC SEQUENCE
# Max input len = 1500 => 15 seconds
maxInputLen = 1500
inputDim = 34

# Reverse input sequence
reverseInputSequence = True

# Devanagari Unicode sequence
# maximum number of Devanagari unicode characters in a line
maxOutputLen = 56
# Numer of possible unicode charaters in the dataset
vocabSize = 128

# Embedding
# OOV +  space + 128 devanagari = 130
embedDim = 130

# LSTM
lstmHiddenDim = 108
depth = 2

# Encoding
encodedDim = 128


##############################################################################
# INPUT
##############################################################################

# Audio MFCC Chunks: list of 18 chunks of lengthx34
audioMfccChunks = split_MFCC_by_audio_times(audioTimesPath=audioTimesPath,
                                            audioMFCCPath=audioMFCCPath)

# Reverse input sequence
if reverseInputSequence:
    for i, chunk in enumerate(audioMfccChunks):
        audioMfccChunks[i] = chunk[::-1]

# Pad input sequence
audioMfccChunksPadded = sequence.pad_sequences(audioMfccChunks,
                                                maxlen=maxInputLen,
                                                padding='pre',
                                                dtype='float')

# Train - Val
valSplit = 0.2
trainX = audioMfccChunksPadded[:int((1 - valSplit) \
                                                * len(audioMfccChunksPadded))]
valX = audioMfccChunksPadded[int((1 - valSplit) \
                                                * len(audioMfccChunksPadded)):]


##############################################################################
# OUTPUT
##############################################################################

# READ DEVANAGARI TEXT

# CHAPTER 15

# File without extras; only with the shlokas, and "__ uvaaca"
# fileName = os.path.join(rootDir, 'docs/BG-clean-C15.txt')
fileName = textPath

# Read file
fileLines = read_unicode_file(fileName)

# Replace with numbers
yIdx = unicode_file_to_idx_sequences(fileLines, pad=True, padding='post',
                                        maxlen=maxOutputLen)

# One hot encode the numbers
Y = np.reshape(np_utils.to_categorical(yIdx, embedDim),
    (yIdx.shape[0], yIdx.shape[1], embedDim))

trainY = Y[:int((1-valSplit)*len(audioMfccChunksPadded))]
valY = Y[int((1-valSplit)*len(audioMfccChunksPadded)):len(audioMfccChunksPadded)]


##############################################################################
# MODEL
##############################################################################

depth = 2

# Input

myInput = Input(shape=(maxInputLen, inputDim,))

# Masking
LSTMinput = Masking(mask_value=0.)(myInput)

# If depth > 1
if depth > 1:
    # First layer
    encoded = LSTM(hiddenDim, activation=LSTMactiv,
                   return_sequences=True)(LSTMinput)
    for d in range(depth - 2):
        encoded = LSTM(hiddenDim, activation=LSTMactiv,
                       return_sequences=True)(encoded)
    # Last layer
    encoded = LSTM(hiddenDim, activation=LSTMactiv)(encoded)
# If depth = 1
else:
    encoded = LSTM(hiddenDim, activation=LSTMactiv)(LSTMinput)

# Encoder
encoded = Dense(encodedDim, activation=encodedActiv)(encoded)


# Encoder
encoder = Sequential()
if depth > 1:
    # First layer
    encoder.add(Bidirectional(LSTM(lstmHiddenDim, return_sequences=True),
        input_shape=(maxInputLen, inputDim)))
    # Intermediate layers
    for d in range(depth - 2):
        encoder.add(Bidirectional(LSTM(lstmHiddenDim, return_sequences=True)
    # Last layer
    encoder.add(Bidirectional(LSTM(lstmHiddenDim, return_sequences=False)
else:
    encoder.add(Bidirectional(LSTM(lstmHiddenDim),
        input_shape=(maxInputLen, inputDim)))
# encoder.add(Dropout(0.5))
encoder.add(Dense(encodedDim, activation='relu'))

# Encoded
encoded = encoder(myInput)

# Decoder Input
decoderInput = RepeatVector(maxOutputLen)(encoded)

# Decoder
decoder = Sequential()
decoder.add(Bidirectional(LSTM(lstmHiddenDim, return_sequences=True),
                        input_shape=(maxOutputLen, encodedDim,)))
decoder.add(TimeDistributed(Dense(embedDim, activation='softmax')))

# Decoded
decoded = decoder(decoderInput)

# Speech Recognizer
speechRecognizer = Model(myInput, decoded)

# Compile
adam = Adam(lr=1e-2)
speechRecognizer.compile(loss='categorical_crossentropy',
            optimizer='rmsprop',
            metrics=['accuracy'])

##############################################################################
# TRAIN
##############################################################################

batchSize = 7
nEpochs = 100
initEpoch = 0

history = speechRecognizer.fit(trainX, trainY, batch_size=batchSize, epochs=nEpochs, verbose=1,
    validation_data=(valX, valY), initial_epoch=initEpoch)
