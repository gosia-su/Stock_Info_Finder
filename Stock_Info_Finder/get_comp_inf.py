import intrinio_data as int_d


def get_comp_inf(query_response):
    df = int_d.get_intrinio_comp_inf(query_response)
    name = df.name
    ticker = df.ticker
    stock_exchange = df.stock_exchange
    short_description = df.short_description
    ceo = df.ceo
    company_url = df.company_url
    business_address = df.business_address
    employees = df.employees
    sector = df.sector
    first_stock_price_date = df.first_stock_price_date
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