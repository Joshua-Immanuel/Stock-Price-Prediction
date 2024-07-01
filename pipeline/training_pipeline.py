from model_trainer import Model_trainer
from datatransformation import Datatransformation
import os
import yaml
import pandas as pd
import numpy as np

class Training_pipeline:
    def __init__(self):
        pass

    def train(self,data):
        data_transformation = Datatransformation()
        x_train, y_train, x_test, y_test , date1, date2 = data_transformation.train_test_split(data)
        model_trainer = Model_trainer()
        print(x_train,y_train)
        self.scale= data_transformation.scale
        model = model_trainer.modelfit(x_train, y_train)
        self.model=model
        y_pred= self.evaluation(x_test,y_test)
        model_trainer.save_model()
        self.save_config()
        y_test = y_test/self.scale
        y_pred =y_pred.ravel()/self.scale
        test_with_dates= pd.DataFrame({'Date': date2, 'y_test': y_test.tolist(), 'y_pred':y_pred.tolist()})
        return test_with_dates

    def evaluation(self,x_test, y_test):
        model=self.model
        y_pred = model.predict(x_test)
        return y_pred


    def save_config(self):
        path = 'artifacts/'
        os.makedirs(path,exist_ok=True)
        file_path = os.path.join(path, 'parameters.yaml')
        data = {'scale':self.scale.tolist()[0]}
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
                