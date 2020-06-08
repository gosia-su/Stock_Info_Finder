import intrinio_data as int_d


def get_news(query_response):
    data = int_d.get_intrinio_news(query_response)
    news1 = data.iloc[0][['title', 'publication_date', 'url', 'summary']]
    news2 = data.iloc[1][['title', 'publication_date', 'url', 'summary']]
    news3 = data.iloc[2][['title', 'publication_date', 'url', 'summary']]
    text = """
            Title: %s
            Release date: %s
            Website link: %s
            Summary: %s\n
            
            Title: %s
            Release date: %s
            Website link: %s
            Summary: %s\n
            
            Title: %s
            Release date: %s
            Website link: %s
            Summary: %s\n
            
             """ \
                % (news1['title'], news1['publication_date'], news1['url'], news1['summary'],
                   news2['title'], news2['publication_date'], news2['url'], news2['summary'],
                   news3['title'], news3['publication_date'], news3['url'], news3['summary'])

    return text

