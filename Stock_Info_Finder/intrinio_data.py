import pandas as pd
import intrinio_sdk

intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0'
security_api = intrinio_sdk.SecurityApi()
company_api = intrinio_sdk.CompanyApi()
fundamentals_api = intrinio_sdk.FundamentalsApi()


def get_intrinio_hp(query):
    identifier = str(query).upper()
    tag = 'adj_close_price'
    api_response = security_api.get_security_historical_data(identifier, tag, page_size=100)
    hist_prices = pd.DataFrame(api_response.historical_data_dict)
    return hist_prices


def get_intrinio_volume(query):
    identifier = str(query).upper()
    api_response = security_api.get_security_price_technicals_adtv(identifier, page_size=1, period=20)
    volume = pd.DataFrame(api_response.technicals_dict)
    return volume


def get_intrinio_wr(query):
    identifier = str(query).upper()
    api_response = security_api.get_security_price_technicals_wr(identifier, page_size=1, period=20)
    wr = pd.DataFrame(api_response.technicals_dict)
    return wr


def get_intrinio_sr(query):
    identifier = str(query).upper()
    api_response = security_api.get_security_price_technicals_sr(identifier, page_size=1, period=20)
    sr = pd.DataFrame(api_response.technicals_dict)
    return sr


def get_intrinio_comp_inf(query):
    identifier = str(query).upper()
    api_response = company_api.get_company(identifier)
    return api_response


def get_intrinio_news(query):
    identifier = str(query).upper()
    api_response = company_api.get_company_news(identifier)
    news = pd.DataFrame(api_response.news_dict)
    return news


def get_intrinio_cf(query):
    identifier = str(query).upper()
    fs_type = '-cash_flow_statement-2019-FY'
    id = identifier+fs_type
    api_response = fundamentals_api.get_fundamental_standardized_financials(id)
    cashflow = pd.DataFrame(api_response.standardized_financials_dict)
    end_date = pd.DataFrame(api_response.fundamental_dict)
    end_date = end_date['end_date'][0]
    end_date = end_date.strftime('%m/%d/%y')
    return cashflow, end_date