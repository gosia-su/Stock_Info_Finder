import requests
import pandas as pd


def get_comp_inf(query_response):
    url_end_point = "https://api-v2.intrinio.com/companies/"
    api_key = "?api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0"
    end_url = url_end_point+str(query_response).upper()+api_key
    data = requests.get(end_url).json()
    df = pd.DataFrame([data])
    name = df['name'][0]
    ticker = df['ticker'][0]
    stock_exchange = df['stock_exchange'][0]
    short_description = df['short_description'][0]
    ceo = df['ceo'][0]
    company_url = df['company_url'][0]
    business_address = df['business_address'][0]
    employees = df['employees'][0]
    sector = df['sector'][0]
    first_stock_price_date = df['first_stock_price_date'][0]
    text_result = f'[Source:  https://intrinio.com/ ]\n\n' \
                  f'Company name:   {name}\n\n' \
                  f'Exchange Ticker:   {ticker}\n\n' \
                  f'Primary exchange:   {stock_exchange}\n\n' \
                  f'Short description:   {short_description}\n\n' \
                  f'Chief Operating Officer:   {ceo}\n\n' \
                  f'Website link:   {company_url}\n\n' \
                  f'Company address:   {business_address}\n\n' \
                  f'Number of employees:   {employees}\n\n' \
                  f'Sector:   {sector}\n\n' \
                  f'First quoted on:   {first_stock_price_date}\n\n'
    return text_result