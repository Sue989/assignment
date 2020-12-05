# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v5MX7qtwagEBD0Kv9gR-gxeSDr5TqiDH
"""

!pip install catboost
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor
import xgboost as xgb
from xgboost import plot_importance, plot_tree
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

plt.style.use('fivethirtyeight')
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/train.csv')
df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y %H:%M')

def create_features(df, label=None):
    """
    Creates time series features from datetime index
    """
    
    df['hour'] = df['date'].dt.hour
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofmonth'] = df['date'].dt.day
    df['quarter'] = df['date'].dt.quarter
    df['weekofyear'] = df['date'].dt.weekofyear
    df['dayofweek'] = df['date'].dt.dayofweek
    df['dayofyear'] = df['date'].dt.dayofyear
    
    
    X = df[['hour','dayofweek','month','year',
           'dayofyear','dayofmonth','weekofyear','quarter']]
    
    if label:
        y = df[label]
        return X, y
    return X
X_train,y=create_features(df, label='speed')
X_train = X_train.to_numpy()
y = y.to_numpy()
from sklearn import preprocessing
# 归一化X，归一化y
scaler_X = preprocessing.StandardScaler()
scaler_X.fit(X_train) 
X_train = scaler_X.transform(X_train)

scaler_y = preprocessing.MinMaxScaler()
scaler_y.fit(y.reshape(-1,1))
y = scaler_y.transform(y.reshape(-1,1))

reg = CatBoostRegressor(n_estimators=5000,
                learning_rate=0.05,
                eval_metric='RMSE',
                loss_function='RMSE',
                
                metric_period=300,
                od_wait=500,
                od_type='Iter',
                depth= 8,
                colsample_bylevel=0.7)

reg.fit(X_train,y)
C = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/test.csv')
C['date'] = pd.to_datetime(C['date'],format='%d/%m/%Y %H:%M')


def create_features(df):
    """
    Creates time series features from datetime index
    """
    
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear
    
    X1 = df[['hour','dayofweek','month','year',
           'dayofyear','dayofmonth','weekofyear','quarter']]
    return X1
X1=create_features(C)
X1=scaler_X.transform(X1)
Y=reg.predict(X1)
Y=scaler_y.inverse_transform(Y.reshape(-1,1))
Y=pd.DataFrame(Y)
Y['id']=C['id']
Y['speed']=Y[0]
del Y[0]
Y.to_csv('y1.csv',index=False,header=1)