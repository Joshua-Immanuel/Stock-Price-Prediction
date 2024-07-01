import numpy as np
import pandas as pd
from datetime import datetime,date
import yfinance as yf

class dataingestion:
    def __init__(self,start_date,end_date,ticker):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker=ticker
    
    def get_stock_prices(self):
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return df

# start='1900-01-01'
# end =date.today()


