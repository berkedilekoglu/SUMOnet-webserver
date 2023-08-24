
from tensorflow.keras import layers, Model, regularizers
from loguru import logger

import os
import sys

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)




class SUMOnet(Model):

    def __init__(self):
        
        super().__init__()
        
        self.cnn = layers.Conv1D(128,2,padding='valid',activation='relu',kernel_initializer='he_normal',strides=1)
        self.bigru = layers.Bidirectional(layers.GRU(16, dropout=0.4, recurrent_dropout=0,return_sequences=True))
        self.pool = layers.GlobalAveragePooling1D()
        self.dense64 = layers.Dense(64,kernel_initializer='he_normal',activity_regularizer= regularizers.l2(1e-4))
        self.dropout = layers.Dropout(0.4)
        self.relu = layers.Activation('relu')
        self.dense128_1 = layers.Dense(128,kernel_initializer='he_normal',activity_regularizer= regularizers.l2(1e-4))
        self.dropout_1 = layers.Dropout(0.4)
        self.relu_1 = layers.Activation('relu')
        self.dense128_2 = layers.Dense(128,kernel_initializer='he_normal',activity_regularizer= regularizers.l2(1e-4))
        self.dropout_2 = layers.Dropout(0.4)
        self.relu_2 = layers.Activation('relu')
        self.dense2 = layers.Dense(2, kernel_initializer='he_normal')
        self.softmax = layers.Activation('softmax')

        self.build((None, 21, 24)) #input shape is batch,21,24

        self.weights_path = os.path.join(os.path.dirname(__file__), 'model_weights', 'sumonet3.h5')
        try:
            super().load_weights(filepath = self.weights_path)
        except FileNotFoundError:
            logger.error(f"Error: Weight file '{self.weights_path}' not found.")
        except Exception as e:
            # Log the exception using Loguru
            logger.exception("Unhandled exception in load_weights:")

    def call(self, inputs):

        x = self.cnn(inputs)
        x = self.bigru(x)
        x = self.pool(x)
        x = self.dense64(x)
        x = self.dropout(x)
        x = self.relu(x)
        x = self.dense128_1(x)
        x = self.dropout_1(x)
        x = self.relu_1(x)
        x = self.dense128_2(x)
        x = self.dropout_2(x)
        x = self.relu_2(x)
        x = self.dense2(x)
        x = self.softmax(x)
        
        return x

    
       

        




