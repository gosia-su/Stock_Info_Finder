import intrinio_data as int_d


def get_cashflow(query_response):
    df, end_date = int_d.get_intrinio_cf(query_response)
    cashflow_items = [f'Cashflow statement for the period ending {end_date}\n\n']
    for i in range(0, df['data_tag'].size):
        name = df.iloc[i]['data_tag']['name']
        value = df.iloc[i]['value']
        unit = df.iloc[i]['data_tag']['unit']
        final_item = name + ':  ' + str(value) + '  (' + str(unit).upper() + ')'
        cashflow_items.append(final_item)
    return '\n'.join(cashflow_items)




