# Keras Bidirectional LSTM IMDB example - https://github.com/fchollet/keras/blob/master/examples/imdb_bidirectional_lstm.py 
# BidirectionalLSTM with masking - http://dirko.github.io/Bidirectional-LSTMs-with-Keras/
# Stateful LSTMs theory - http://philipperemy.github.io/keras-stateful-lstm/

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional

# MFCC sequence
maxInputLen = ??
inputDim = 13

# Devanagari Unicode sequence
# maximum number of Devanagari unicode characters in a line
maxOutputLen = 56
# Numer of possibleunicode charaters in the dataset
outputDim = 128

# Embedding
# OOV +  space + 128 devanagari = 130
embedDim = 130

# LSTM
lstmHidDim = 108

# Encoding
encodedDim = 128

#INPUT

# Read mp3 file

# Split into frames

# Pre-pad input sequences
X = sequence.pad_sequences(myInput, maxlen=maxInputLen, padding='pre')

# OUTPUT

# CHAPTER 01

# File without extras; only with the shlokas, and "__ uvaaca"         
fileName = '/home/voletiv/BG_clean_C01.txt'
# Read all characters
with open(fileName, encoding='utf-8') as f:
    fileText01 = f.read()
# Split lines
fileLines01 = fileText01.split('\n')

# Replace with numbers
# 0 = OOV, 1 = space, 2 = \u0900, ... 101 = stopChar = '|', ... 129 = \u097F
y = fileLines01
yIdx = []
# Convert to numbers (starting at 1)
for line in y:
    yLine = []
    for char in line:
        if char == ' ':
            yLine.append(1)
        else:
            yLine.append(ord(char) - ord('\u0900') + 1)
    yIdx.append(yLine)

# Post-pad output sequences with 0
Y = sequence.pad_sequences(yIdx, maxlen=maxOutputLen, padding='post')

# MODEL

myInput = Input(shape=(maxInputLen, inputDim,))

# Encoder
encoder = Sequential()
encoder.add(Bidirectional(LSTM(lstmHidDim, input_shape=(maxInputLen, inputDim))))
# encoder.add(Dropout(0.5))
encoder.add(Dense(encodedDim, activation='sigmoid'))

encoded = encoder(myInput)



# Decoder
decoder = Sequential()
decoder.add(Bidirectional(LSTM(lstmHidDim, input_shape=(encodedDim))))
# decoder.add(Dropout(0.5))
decoder.add(Dense(encodedDim, activation='sigmoid'))


model.add(Embedding(inputDim, embedDim, input_length=maxInputLen))

