import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import pickle

def train_model():
    df = pd.read_csv('cow_prices.csv', parse_dates=['date'], index_col='date')
    model = ARIMA(df['price'], order=(5, 1, 0))
    model_fit = model.fit()
    with open('cow_price_model.pkl', 'wb') as f:
        pickle.dump(model_fit, f)

def forecast_price(days=30):
    with open('cow_price_model.pkl', 'rb') as f:
        model_fit = pickle.load(f)
    forecast = model_fit.forecast(steps=days)
    return forecast
