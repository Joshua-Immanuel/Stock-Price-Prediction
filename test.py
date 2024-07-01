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
import boto3

tf.config.set_visible_devices([], 'GPU')

start='1900-01-01'
end =datetime.today().strftime('%Y-%m-%d')

df = yf.download('MSFT', start='2001-01-01', end=end)
# df=df.reset_index()
print(df.head())
# z=Training_pipeline().train(df)
# print(z)
# model= load_model('artifacts/model.h5')
# p= Predict_pipeline().predict('2024-07-21',df,model)
# print(p)