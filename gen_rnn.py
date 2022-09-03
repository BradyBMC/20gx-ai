import pickle
import melee

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping


physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
    
x0 = [] # x0
x1 = [] # y0
x2 = [] # x1
x3 = [] # y1
y = []

timestep = 48

for i in range(len(data) - timestep):

    sample = data[i:i+48]

    x0.append([x[0][0] for x in sample])
    x1.append([x[0][1] for x in sample])
    
    x2.append([x[0][2] for x in sample])
    x3.append([x[0][3] for x in sample])
    
    y.append(data[i+48][1])

x0, x1 = np.array(x0, dtype=float), np.array(x1, dtype=float)
x2, x3 = np.array(x2, dtype=float), np.array(x3, dtype=float)
y = np.array(y, dtype=float)

scaler = MinMaxScaler(feature_range=(0,1))
x0 = scaler.fit_transform(x0)
x1 = scaler.fit_transform(x1)
x2 = scaler.fit_transform(x2)
x3 = scaler.fit_transform(x3)
y = scaler.fit_transform(y)

x = np.stack([x0, x1, x2, x3], axis=2)

X_train, X_test = x[:-480], x[-480:]
Y_train, Y_test = y[:-480], y[-480:]

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x.shape[1], x.shape[2])))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(50, activation='relu'))
model.add(Dense(10))

filepath = 'models/{epoch:02d}-{loss:.4f}-val_loss:.4f}-{mae:.4f}-{val_mae:.4f}.hdfs'
callbacks = [EarlyStopping(monitor='val_loss', patience=20),
             ModelCheckpoint(filepath, monitor='loss', save_best_only=True, mode='min')]

optimizers.SGD(momentum=0.9)
model.compile(optimizer='SGD', loss='mse', metrics=['mae'])

model.fit(X_train, Y_train, validation_split=0.2, epochs=1000, callbacks=callbacks, batch_size=16)