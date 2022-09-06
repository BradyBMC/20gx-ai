import pickle
import melee

import numpy as np
import tensorflow as tf
from numpy import array
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

def split_data(data, timestep):
    # contains the x,y coord for both players
    x0, x1, x2, x3 = list(), list(), list(), list()
    y = list()

    for i in range(len(data) - timestep):

        end = i + timestep
    
        sample = data[i:end]

        x0.append([x[0][0] for x in sample])
        x1.append([x[0][1] for x in sample])
    
        x2.append([x[0][2] for x in sample])
        x3.append([x[0][3] for x in sample])
    
        y.append(data[timestep][1])

    return array(x0, dtype=float), array(x1, dtype=float), array(x2, dtype=float), array(x3, dtype=float), array(y, dtype=float)

# data length of frames in game, contains x,y of both players
# and controller inputs of falcon
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

timestep = 48
# x0 is a list the length of frames in a game.
# where each index is length of 48 timestep

x0, x1, x2, x3, y = split_data(data, timestep)

# Sigmoid function equivalent to make range 0 to 1
'''
scaler = MinMaxScaler(feature_range=(0,1))
x0 = scaler.fit_transform(x0)
x1 = scaler.fit_transform(x1)
x2 = scaler.fit_transform(x2)
x3 = scaler.fit_transform(x3)
y = scaler.fit_transform(y)
'''

# stacks the training data to have [x0, x1, x2, x3] as 1 timestep
# 48 timesteps are 1 training sample
x = np.stack([x0, x1, x2, x3], axis=2)

model = Sequential()
'''
model.add(LSTM(50, activation='relu', input_shape=(x.shape[1], x.shape[2])))
model.add(Dense(10))
model.compile(optimizer='adam', loss='mse')
model.fit(x, y, epochs=200, verbose=0)
'''
model.add(LSTM(50, return_sequences=True, activation='relu', input_shape=(x.shape[1], x.shape[2])))
model.add(LSTM(50, return_sequences=False, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(10))



filepath = 'models/{epoch:02d}-{loss:.4f}-{val_loss:.4f}-{mae:.4f}-{val_mae:.4f}.hdf5'
callbacks = [EarlyStopping(monitor='val_loss', patience=20),
             ModelCheckpoint(filepath, monitor='loss', save_best_only=True, mode='min')]

optimizers.SGD(momentum=0.9)


model.compile(optimizer='adam', loss='mse', metrics=['mae'])
# model.fit(x, y, epochs=200, verbose=0)
model.fit(x, y, validation_split=0.2, epochs=200, callbacks=callbacks, batch_size=16)