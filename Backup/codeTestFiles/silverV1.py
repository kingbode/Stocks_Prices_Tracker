
import requests
from bs4 import BeautifulSoup


def get_silver_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
    }

    params = {
        'currency': 'KWD',
        'amount': '1',
    }

    if url == 'https://www.livepriceofgold.com/silver-price/kuwait.html':
        div_class = "sekme-content"

    elif url == 'https://www.prokerala.com/finance/silver-price.php':
        div_class = "highlight highlight-blue"


    try:

        response = requests.get(url, params= params , headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            silver_prices_data = soup.find_all('div', class_=div_class)[0]
            silver_price = silver_prices_data.find_all('tr')[1]
            silver_price = silver_price.find_all('td')[1].text.replace("KWD", "").strip()
            # print(silver_price)

            if silver_price:
                return silver_price
            else:
                return None

    except Exception as e:
        print(f'Error fetching data from the website {url} and the error is: {e} ')
        return None

def main():

    urls = ['https://www.livepriceofgold.com/silver-price/kuwait.html',
            'https://www.prokerala.com/finance/silver-price.php']

    for url in urls:
        get_silver_price(url)


if __name__ == '__main__':
    main()
