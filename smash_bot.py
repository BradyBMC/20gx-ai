import pickle
import melee
import os
import glob

import numpy as np
import tensorflow as tf
from numpy import array
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import load_model

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
    
        y.append(data[end][1])

    x0, x1= array(x0, dtype=float), array(x1, dtype=float)
    x2, x3 = array(x2, dtype=float), array(x3, dtype=float)
    y = array(y, dtype=float)
    
    '''
    Data normalization: transforms features of differing ranges to universal range
    Needed to allow quicker convergence of gradient descent
    '''
    scaler = MinMaxScaler(feature_range=(0,1))
    x0 = scaler.fit_transform(x0)
    x1 = scaler.fit_transform(x1)
    x2 = scaler.fit_transform(x2)
    x3 = scaler.fit_transform(x3)
    y = scaler.fit_transform(y)

    # Stacks a list of features consisting of 48 timesteps as 1 sample
    return np.stack([x0, x1, x2, x3], axis=2), y

class SmashBot:
    def __init__(self,
                 data,
                 timestep=48,
                 load: bool=False
                ):

        self.x, self.y = split_data(data, timestep)
        # self.timestep=timestep
        
        # Check if model_path directory legal
        if load is False:
            self.model = self.create_bot()
        else:
            self.model = self.load_bot()
        
        filepath = 'models/{epoch:02d}-{loss:.4f}-{val_loss:.4f}-{mae:.4f}-{val_mae:.4f}.hdf5'
        callbacks = [EarlyStopping(monitor='val_loss', patience=20),
                     ModelCheckpoint(filepath, monitor='loss', save_best_only=True, mode='min')]
        self.callbacks=callbacks
        
    # Create model
    def create_bot(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, activation='relu', input_shape=(self.x.shape[1], 
                                                                                  self.x.shape[2])))
        model.add(LSTM(50, return_sequences=False, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(10))
        return model

    # Load model from the model path
    def load_bot(self):
        path = 'models'
        file_list = glob.glob('models/*.hdf5')
        latest_file = max(file_list, key=os.path.getctime)
        print('\nModel loaded\n', latest_file,'\n')
        return load_model(latest_file)

    def train_model(self):
        # x, y = split_data(data, self.timestep)
        optimizers.SGD(momentum=0.9)
        self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        self.model.fit(self.x, self.y, validation_split=0.2, epochs=200, callbacks=self.callbacks, batch_size=16)
        

with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
obj = SmashBot(data, load=True)
obj.train_model()

'''
path = 'pdata'
directory = os.fsencode(path)
for file in os.listdir(directory):
        filename = path + '/' + os.fsdecode(file)
        assert filename.endswith('.pkl'), 'Contains non .pkl files: ' + filename
        print('\nTraining pkl loaded', filename,'\n')
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        obj = SmashBot(data, load=True)
        obj.train_model()
'''