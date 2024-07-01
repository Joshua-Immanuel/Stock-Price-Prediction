import tensorflow as tf
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
import os


class Model_trainer:
    def __init__(self):
        tf.config.set_visible_devices([], 'GPU')
    
    def dlmodel(self,x_train):
        model = Sequential()
        model.add(LSTM(units=50, activation = 'relu',return_sequences= True, input_shape= (x_train.shape[1],1)))
        model.add(Dropout(0.2))

        model.add(LSTM(units=60, activation = 'relu',return_sequences= True))
        model.add(Dropout(0.3))

        model.add(LSTM(units=80, activation = 'relu',return_sequences= True))
        model.add(Dropout(0.4))

        model.add(LSTM(units=120, activation = 'relu'))
        model.add(Dropout(0.5))

        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def modelfit(self, x_train, y_train):
        model = self.dlmodel(x_train)

        model.fit(x_train, y_train, epochs=1)
        self.model = model
        return model
    
    def save_model(self):
        model_path = 'artifacts/'
        os.makedirs(model_path,exist_ok=True)
        self.model.save(model_path+"model.h5")
