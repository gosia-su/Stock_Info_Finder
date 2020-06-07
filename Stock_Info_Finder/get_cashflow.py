import requests
import pandas as pd


def get_cashflow(query_response):
    url_end_point = "https://api-v2.intrinio.com/fundamentals/"
    statement = "-cash_flow_statement-2019-FY/standardized_financials?"
    api_key = "api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0"
    end_url = url_end_point + str(query_response).upper() + statement + api_key
    data = requests.get(end_url).json()
    df = pd.DataFrame(data['standardized_financials'])
    end = pd.DataFrame(data['fundamental'])['end_date'][0]
    cashflow_items = [f'Cashflow statement for the period ending {end}\n\n']
    for i in range(0, df['data_tag'].size):
        name = df.iloc[i]['data_tag']['name']
        value = df.iloc[i]['value']
        unit = df.iloc[i]['data_tag']['unit']
        final_item = name + ':  ' + str(value) + '  (' + str(unit).upper() + ')'
        cashflow_items.append(final_item)
    return '\n'.join(cashflow_items)




