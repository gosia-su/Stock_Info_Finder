import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import requests


def get_historical_prices(query_response):
    end_url = 'https://api-v2.intrinio.com/securities/'
    api_key = '/historical_data/adj_close_price?api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0'
    url = end_url + str(query_response).upper() + api_key
    data = requests.get(url).json()
    data = pd.DataFrame(data['historical_data'])
    data = data.sort_values(by=['date']).reset_index().drop(columns='index')
    data = data.set_index('date')

    return data


def get_predictions(query_response):
    data = get_historical_prices(query_response)
    forecast_days = 15
    data['prediction'] = data['value'].shift(-forecast_days)

    # independent data set
    ind = np.array(data.drop(['prediction'], 1))
    ind = ind[:-forecast_days]

    # dependent data set
    dep = np.array(data['prediction'])
    dep = dep[:-forecast_days]

    # set for predictions
    ind_forecast = np.array(data.drop(['prediction'], 1))[-forecast_days:]

    # create test and train sets
    ind_train, ind_test, dep_train, dep_test = train_test_split(ind, dep, test_size=0.2)

    # Support Vector Machine model
    my_svr = SVR(kernel='rbf', C=1e3, gamma=0.01)
    my_svr.fit(ind_train, dep_train)
    svm_confidence = round(my_svr.score(ind_train, dep_train), 6)
    svm_prediction = my_svr.predict(ind_forecast)
    svm_prediction = pd.DataFrame(svm_prediction).iloc[:, 0]

    # Linear Regression Model
    my_lr = LinearRegression()
    my_lr.fit(ind_train, dep_train)
    lr_confidence = round(my_lr.score(ind_train, dep_train),6)
    lr_prediction = my_lr.predict(ind_forecast)
    lr_prediction = pd.DataFrame(lr_prediction).iloc[:, 0]

    final_wording = (f'Future prices are predicted using two models: Linear Regression and Support Vector Machine.\n'
                     f'Note: parameters used for SVM => kernel: rbf, C: 1e3, gamma: 0.01\n\n'
                     f'LR confidence: {lr_confidence}\n'
                     f'LR predicted prices for future {forecast_days} trading days:\n{lr_prediction}\n\n'
                     f'SVM confidence: {svm_confidence}\n'
                     f'SVM predicted prices for future {forecast_days} trading days:\n{svm_prediction}\n\n')

    data_for_chart = pd.DataFrame(data['value'].iloc[-forecast_days-10:])
    for i in range(forecast_days):
        data_for_chart = data_for_chart.append(pd.Series(), ignore_index=True)
    data_for_chart['svm_d'] = svm_prediction
    data_for_chart['svm'] = data_for_chart['svm_d'].shift(forecast_days + 10)
    data_for_chart['lr_d'] = lr_prediction
    data_for_chart['lr'] = data_for_chart['lr_d'].shift(forecast_days + 10)
    data_for_chart = data_for_chart.drop(['svm_d', 'lr_d'], 1)

    return final_wording, data_for_chart

