#!/usr/bin/env python
import numpy as np
from math import *

from board import DotsBoard

from sklearn.model_selection import train_test_split

from keras.layers import Input, Dense, Conv2D, Flatten, Activation, \
    Multiply, Lambda, Reshape, Concatenate
from keras.models import Model
from keras.models import model_from_json
from keras import regularizers
import keras.backend as K

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class PolicyNet:

    def __init__(self, n=10000):
        self.create_model()

    def create_model(self):
        # Define input shape
        inputs = Input(shape=(10,10,3))
    
        # Add layers
        x = Conv2D(64, (3, 3), padding='same', activation='relu',
                   data_format = 'channels_last')(inputs)
        x = Conv2D(64, (3, 3), padding='same', activation='relu',
                   data_format = 'channels_last')(x)
        x = Conv2D(64, (3, 3), padding='same', activation='relu',
                   data_format = 'channels_last')(x)
        x = Conv2D(64, (3, 3), padding='same', activation='relu',
                   data_format = 'channels_last')(x)
        x = Conv2D(64, (3, 3), padding='same', activation='relu',
                   data_format = 'channels_last')(x)
        x = Conv2D(64, (3, 3), padding='same', activation='relu',
                   data_format = 'channels_last')(x)

        # Policy head
        #turn_plane = Lambda(lambda z: z[:,:,:,2])(inputs)
        #turn_plane = Reshape((10,10,1))(turn_plane)
        #x = Concatenate(axis=-1)([x, turn_plane])
        
        x = Conv2D(1, (1,1), activation=None)(x)
        x = Flatten()(x)
    
        #x = Dense(100, use_bias=True, activation=None,
        #          kernel_regularizer=regularizers.l2(0.001),
        #          bias_regularizer = None)(x)
        # Filter out impossible moves
        mask = Lambda(lambda z: z[:,:,:,1])(inputs)
        mask = Flatten()(mask)
        x = Multiply()([mask, x])
    
        predictions = Activation('softmax')(x)
        
        # Compile the model
        self.model = Model(inputs=inputs, outputs=predictions)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy',
                      metrics=['categorical_accuracy'])

    
    def train(self, n_epochs = 3):
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y,
                                                            test_size=0.10)

        
        self.model.fit(X_train, Y_train,
                       validation_data=(X_test, Y_test),
                       epochs=n_epochs, batch_size=32)

    
    def load_data(self, n=None, augmented=True):
        move_action_pairs = []
        if augmented:
            filename = 'data/expert_moves_augmented.dat'
        else:
            filename = 'data/expert_moves.dat'

        num_lines = sum(1 for line in open(filename))
        print 'loading %d position/move pairs' % num_lines
        
        
        if n is None:
            
            X = np.zeros((num_lines, 10, 10, 3), dtype=np.uint8)
            Y = np.zeros((num_lines, 10, 10, 1), dtype=np.uint8)
            i = 0
            with open(filename, 'r') as f:
                line = f.readline()
                while line:
                    position, move0, move1 = line.split(' ')
                    position = np.array(list(position),
                                        dtype = np.uint8).reshape((10,10,3))
                    X[i, ...] = position
                    Y[i, int(move0), int(move1), 0] = 1
                    
                    i += 1
                    if i % 25000 == 0:
                        print i
                    line = f.readline()

            self.X = X
            self.Y = Y.reshape(self.X.shape[0], -1)
            

        #print 'splitlines succesful'


        else:
            with open(filename, 'r') as f:
                lines = f.read().splitlines()
            if n is None or n>len(lines):
                n = len(lines)
            idxs = np.random.randint(len(lines), size = n)
            
            for idx in idxs:
                position, move0, move1 = lines[idx].split(' ')
                position = np.array(list(position), dtype = np.uint8).reshape((10,10,3))
                move = (int(move0), int(move1))
                move_action_pairs.append((position, move))

            positions, moves = zip(*move_action_pairs)
        
            self.X = np.concatenate([aux[np.newaxis, ...]
                                     for aux in positions], axis=0)
            self.Y = np.zeros((self.X.shape[0], 10, 10, 1))

            for i, move in enumerate(moves):
                self.Y[i, move[0], move[1], 0] = 1
            self.Y = self.Y.reshape(self.X.shape[0], -1)
        

                
    def save_to_disk(self):
        # serialize model to JSON
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights("model.h5")
        print("Saved model to disk")

    def load_from_disk(self):
        # load json and create model
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")
        self.model = loaded_model
    

    
if __name__ == '__main__':


    model = PolicyNet()
    
    print 'loading data...'    
    model.load_data(n = 10000000, augmented=False)
    model.train(n_epochs = 10)

    model.save_to_disk()
    
    
    
