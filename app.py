# import pandas as pd
# from keras.models import load_model
# import streamlit as st
# import tensorflow as tf
# from datetime import datetime
# import plotly.graph_objects as go
# from dataingestion import dataingestion
# from pipeline.training_pipeline import Training_pipeline
# from pipeline.predcit_pipeline import Predict_pipeline
# import os.path
# import boto3


from pipeline.training_pipeline import Training_pipeline
from pipeline.predcit_pipeline import Predict_pipeline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from keras.models import load_model
import streamlit as st
import tensorflow as tf
from datetime import datetime
import plotly.graph_objects as go
from dataingestion import dataingestion
import os.path
import boto3

tf.config.set_visible_devices([], 'GPU')

start='2001-01-01'
end = datetime.today().strftime('%Y-%m-%d')

st.title('Stock Trend Prediction')

user_input =st.text_input('Enter stock ticker','MSFT')
df= dataingestion(start,end,user_input).get_stock_prices()


st.subheader(f'Data from start to {end}')
st.write(df.describe())
st.subheader(f'Closing Price vs Time chart')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Closing Price'))
fig.update_layout(title='Closing Price vs Time',
                  xaxis_title='Date',
                  yaxis_title='Closing Price')
st.write(
    fig
)

st.subheader(f'Closing Price vs Moving Average chart')
ma100 = df['Close'].rolling(window=100).mean()
ma200 = df['Close'].rolling(window=200).mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Closing Price'))
fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='100-day MA', visible='legendonly'))
fig.add_trace(go.Scatter(x=df.index, y=ma200, mode='lines', name='200-day MA', visible='legendonly'))
fig.update_layout(
    title='Closing Price vs Time',
    xaxis_title='Date',
    yaxis_title='Closing Price'
)
show_ma = st.checkbox('Show Moving Averages',value=True)

if show_ma:
    fig.update_traces(visible=True, selector=dict(name='100-day MA'))
    fig.update_traces(visible=True, selector=dict(name='200-day MA'))
else:
    fig.update_traces(visible=False, selector=dict(name='100-day MA'))
    fig.update_traces(visible=False, selector=dict(name='200-day MA'))
st.plotly_chart(fig, width=1000, height=500)

model_path = 'artifacts/model.h5'
if not os.path.exists(model_path):
    date_test_pred = Training_pipeline().train(df)
    df_json = pd.DataFrame(date_test_pred)
    df_json['Date'] = pd.to_datetime(df_json['Date'])
    st.subheader('Actual and Predicted Values Over Time')
    fig_json = go.Figure()
    fig_json.add_trace(go.Scatter(x=df_json['Date'], y=df_json['y_test'], mode='lines', name='Actual'))
    fig_json.add_trace(go.Scatter(x=df_json['Date'], y=df_json['y_pred'], mode='lines', name='Predicted'))
    fig_json.update_layout(xaxis_title='Date',
                        yaxis_title='Closing Price')
    st.plotly_chart(fig_json, width=1000, height=500)
    
# s3 = boto3.client('s3')
# s3 = boto3.resource(
#     service_name='s3'
# )
# s3.Bucket('stockmodels9').upload_file(Filename='artifacts/model.h5', Key='model.h5')
model= load_model('artifacts/model.h5')

st.subheader('Predict future stock')
input_date =st.text_input('YYYY-MM-DD')

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
if input_date:
        if is_valid_date(input_date):
            st.success(f'{input_date} is a valid date.')
        else:
            st.error(f'{input_date} is not a valid date.')


if is_valid_date(input_date):
     predict=Predict_pipeline().predict(input_date,df,model)
     predict['Prediction'] = predict['Prediction'].apply(lambda x: x[0])
     print(predict['Prediction'])
     predict['Date'] = pd.to_datetime(predict['Date'])
     st.subheader('Predicted Values Over Time')
     fig_json = go.Figure()
     fig_json.add_trace(go.Scatter(x=predict['Date'], y=predict['Prediction'], mode='lines', name='Predicted'))
     fig_json.update_layout(title='Predicted Values Over Time',
                        xaxis_title='Date',
                        yaxis_title='Prediction')
     st.plotly_chart(fig_json, width=1000, height=500)


