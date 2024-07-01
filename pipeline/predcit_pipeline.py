from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import yaml
from datatransformation import Datatransformation
import streamlit as st

class Predict_pipeline:
      def __init__(self):
            file_path = 'artifacts/parameters.yaml'

            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            self.scale=data['scale']
            pass
      
      def predict(self,date, df, model):
            df = df.reset_index()
            input_data, scale = Datatransformation().transform(pd.DataFrame(df['Close']))
            pred = []
            pred_dates = [] 
            date_string1 = date
            date_string2 = df['Date'].iloc[-1].date().strftime('%Y-%m-%d')
            date1 = datetime.strptime(date_string1, '%Y-%m-%d')
            date2 = datetime.strptime(date_string2, '%Y-%m-%d')
            
            diff = abs((date1 - date2).days)
            days_placeholder = st.empty()
            diff1= diff
            while diff > 0:
                print(diff," days*")
                days_placeholder.write(f"{diff1-diff} days/")
                diff -= 1

                last_100 = input_data[-100:]
                stock = model.predict(np.expand_dims(last_100, axis=0))
                # print(stock)
                input_data = np.vstack([input_data, stock])
                pred.append(np.ravel(stock /self.scale))

                pred_date = date1 - timedelta(days=diff)
                pred_dates.append(pred_date)
            predictions_with_dates = pd.DataFrame({'Date': pred_dates, 'Prediction': pred})
            return predictions_with_dates

