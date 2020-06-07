import requests
import pandas as pd


def get_data_for_analysis(query_response):
    url_end_point = "https://api-v2.intrinio.com/securities/"
    api_key = "/historical_data/adj_close_price?api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0"
    end_url = url_end_point + str(query_response).upper() + api_key
    data = requests.get(end_url).json()
    hist_prices = pd.DataFrame(data['historical_data'])
    hp_trans = hist_prices.sort_values(by=['date']).reset_index().drop(columns='index')
    hp_trans['date'] = pd.to_datetime(hp_trans['date'])
    hp_trans['date'] = hp_trans['date'].dt.strftime('%m/%d/%y')
    hp_trans['roll_mean'] = hp_trans.iloc[:, 1].rolling(window=20).mean()
    hp_trans['std'] = hp_trans.iloc[:, 1].rolling(window=20).std()
    hp_trans['lower_band'] = hp_trans['roll_mean'] - 2 * hp_trans['std']
    hp_trans['upper_band'] = hp_trans['roll_mean'] + 2 * hp_trans['std']
    hp_trans['interday_return'] = hp_trans['value'].pct_change()
    hp_final_index = hp_trans.set_index('date')
    hp_final = hp_final_index.loc[hp_final_index['roll_mean'].notnull() == True]
    return hp_final


def get_avg_volume(query_response):
    url_end_point = "https://api-v2.intrinio.com/securities/"
    api_key = "/prices/technicals/adtv?api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0"
    end_url = url_end_point + str(query_response).upper() + api_key
    data = requests.get(end_url).json()
    df = pd.DataFrame(data['technicals'])
    end_date = pd.to_datetime(df.iloc[0]['date_time']).strftime('%m/%d/%y')
    end_value = round(float(df.iloc[0]['adtv']), 2)
    final_text = f'Average daily trading volume as of {end_date} was {end_value} shares.'
    return final_text


def get_wr(query_response):
    url_end_point = "https://api-v2.intrinio.com/securities/"
    api_key = "/prices/technicals/wr?api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0"
    end_url = url_end_point + str(query_response).upper() + api_key
    data = requests.get(end_url).json()
    df = pd.DataFrame(data['technicals'])
    end_date = pd.to_datetime(df.iloc[0]['date_time']).strftime('%m/%d/%y')
    end_value = round(float(df.iloc[0]['wr']), 2)
    if end_value < -80:
        final_text = f'Williams %R as of {end_date} is {end_value}, which may indicate that {str(query_response).upper()} shares are oversold.'
    elif end_value > -20:
        final_text = f'Williams %R as of {end_date} is {end_value}, which may indicate that {str(query_response).upper()} shares are overbought.'
    else:
        final_text = f'Williams %R as of {end_date} is {end_value}.'
    return final_text


def get_os(query_response):
    url_end_point = "https://api-v2.intrinio.com/securities/"
    api_key = "/prices/technicals/sr?api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0"
    end_url = url_end_point + str(query_response).upper() + api_key
    data = requests.get(end_url).json()
    df = pd.DataFrame(data['technicals'])
    end_date = pd.to_datetime(df.iloc[0]['date_time']).strftime('%m/%d/%y')
    end_value = round(float(df.iloc[0]['sr']), 2)
    if end_value > 80:
        final_text = f'Stochastic Oscillator level as of {end_date} is {end_value}, which may indicate that {str(query_response).upper()} shares are overbought.'
    elif end_value < 20:
        final_text = f'Stochastic Oscillator level as of {end_date} is {end_value}, which may indicate that {str(query_response).upper()} shares are oversold.'
    else:
        final_text = f'Stochastic Oscillator level as of {end_date} is {end_value}.'
    return final_text


def get_stock_trend(query_response):
    hp_final = get_data_for_analysis(query_response)
    start_date = hp_final.index.min()
    end_date = hp_final.index.max()
    price_start = round(hp_final['value'].loc[start_date], 2)
    price_end = round(hp_final['value'].loc[end_date], 2)
    high_price = hp_final['value'].nlargest(1)
    high_price_value = round(high_price.iloc[0], 2)
    high_price_date = high_price.index.values[0]
    low_price = hp_final['value'].nsmallest(1)
    low_price_value = round(low_price.iloc[0], 2)
    low_price_date = low_price.index.values[0]
    change_abs = round(price_end - price_start, 2)
    change_percent = round((change_abs)/price_start*100, 2)
    if change_abs > 0:
        price_change = f'increase of $ {change_abs} (by {change_percent}%)'
    else:
        price_change = f'decrease of $ {change_abs} (by {change_percent}%)'
    std_ir = hp_final['interday_return'].std(skipna=True)
    annualized_volatility = round((252 ** (1/2)) * std_ir*100, 2)
    stock_name = str(query_response).upper()
    avg_trading_volume = get_avg_volume(query_response)
    wr = get_wr(query_response)
    os = get_os(query_response)
    writeup = f"Analysis period for {stock_name} historical performance covers timespan between {start_date} and {end_date}.\n" \
              f"Analysis is based on daily adjusted close prices recorded on the security's primary stock exchange.\n\n" \
              f"{stock_name} stock price started at $ {price_start} and ended at $ {price_end}, which constitutes {price_change} over analysed period.\n\n" \
              f"Highest price of $ {high_price_value} was quoted on {high_price_date}. Lowest price of $ {low_price_value} was quoted on {low_price_date}.\n\n" \
              f"Annualized stock price volatility calculated based on performance during analysis period is {annualized_volatility}%.\n\n" \
              f"{avg_trading_volume}\n\n" \
              f"{wr}\n\n" \
              f"{os}\n\n"
    return writeup

