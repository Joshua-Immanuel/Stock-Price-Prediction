import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Datatransformation:
    def __init__(self):
      pass

    def transform(self,data):
      scaler = MinMaxScaler(feature_range=(0,1))
      data_array = scaler.fit_transform(data)
      return data_array, scaler.scale_
    
    def split(self,data_array):
        x = []
        y = []

        for i in range(100,data_array.shape[0]):
            x.append(data_array[i-100:i])
            y.append(data_array[i,0])
        x, y = np.array(x),np.array(y)

        return x, y

    def train_test_split(self,df):
        
        df=df.reset_index()
        df=df.drop(['Adj Close'],axis=1)
        data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.9)])
        data_training_date= df['Date'][0:int(len(df)*0.9)].tolist()
        data_testing = pd.DataFrame(df['Close'][int(len(df)*0.9):])
        data_testing_date = df['Date'][int(len(df)*0.9):].tolist()
        data_tarining_array, scale1 = self.transform(data_training)
        x_train, y_train = self.split(data_tarining_array)
        past_100days = data_training.tail(100)
        final_df = pd.concat([past_100days, data_testing], ignore_index=True)
        data_testing_array , scale = self.transform(final_df)
        x_test, y_test = self.split(data_testing_array)
        self.scale= scale1
        self.input_data = data_testing_array
        return x_train, y_train, x_test, y_test , data_training_date , data_testing_date


