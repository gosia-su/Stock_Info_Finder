import requests
import pandas as pd


def get_news(query_response):
    url_end_point = "https://api-v2.intrinio.com/companies/"
    api_key = "/news?api_key=OjJiZDM3OWU0ZTI0YmM5YTdhNzY1NjIwZjczZGRjMjg0"
    end_url = url_end_point+str(query_response).upper()+ api_key
    data = requests.get(end_url).json()
    latest_news = data['news'][0:3]
    df = pd.DataFrame(latest_news)
    news1 = df.iloc[0][['title', 'publication_date', 'url', 'summary']]
    news2 = df.iloc[1][['title', 'publication_date', 'url', 'summary']]
    news3 = df.iloc[2][['title', 'publication_date', 'url', 'summary']]
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

