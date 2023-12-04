from bs4 import BeautifulSoup
import convert_numbers
from datetime import datetime
import aiohttp
import asyncio
import time
import matplotlib.pyplot as plt
import json
import os

def get_stocks_data():
    # read the stocks dict from the stocks.json file
    try:
        with open('stocks.json', 'r') as f:
            stocks = json.load(f)

            for stock_type, stock_data in stocks.items():
                stock_data['get_price_function'] = eval(stock_data['get_price_function'])
            if not stocks:
                return -1

        return stocks
    except FileNotFoundError:
        print('stocks.json file not found')
        return None


async def get_gold_price24_async(url, _key):
    """
   This function takes an url and returns the gold price from that url
   :param url:
   :param _key:
   :return: float - the gold price
    """
    try:
        async with (aiohttp.ClientSession() as session):
            async with session.get(url) as response:
                page_content = await response.text()
                soup = BeautifulSoup(page_content, 'html.parser')

                if url == 'https://www.livepriceofgold.com/':
                    gold_price24 = soup.find('div', class_="currencyt-h").find_all('table')[1].find_all('tr')[10]
                    gold_price24 = gold_price24.find_all('td')[1].text.replace("KWD", "").strip()
                    gold_price24 = float(gold_price24)
                else:
                    gold_price24 = soup.find_all('tbody')[0].find_all('tr')[0].find_all('td')[1]
                    gold_price24 = gold_price24.text.replace("KWD", "").strip()
                    if url == 'https://wikigerman.net/gold-kw/':
                        gold_price24 = float(gold_price24)
                    else:
                        gold_price24 = float(convert_numbers.hindi_to_english(gold_price24)) / 1000

                return gold_price24, _key, url

    except Exception as e:
        print(f'Error fetching data from the website {url} and the error is: {e} ')
        return None


def update_stock_price_json_file(stock_type, stock_average_price):
    """
    This function takes the average gold price and updates the gold_prices.json file
    :param stock_type:
    :param stock_average_price:
    :return: None
    """
    print('\nUpdating the gold_prices.json file .......', end='')

    file_name = f'{stock_type.lower()}_prices.json'

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            new_update = {
                'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'price': stock_average_price
            }

            # check and the status of the price either it is the same or changed
            last_price = data[-1]['price']
            current_price = stock_average_price

            if last_price > current_price:
                print(f'\nThe {stock_type} price is decreased by {(last_price - current_price):.3f} KD')
            elif last_price < current_price:
                print(f'\nThe {stock_type} price is increased by {(current_price - last_price):.3f} KD')
            else:
                print(f'\nThe {stock_type} price is not changed')

            data.append(new_update)

        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

    else:
        with open(file_name, 'w') as file:
            new_update = {
                'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'price': stock_average_price
            }
            json.dump([new_update], file, indent=4)

    print(' Done')


async def get_silver_price_async(url, _key):
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

    div_class = None

    if url == 'https://www.livepriceofgold.com/silver-price/kuwait.html':
        div_class = "sekme-content"

    elif url == 'https://www.prokerala.com/finance/silver-price.php':
        div_class = "highlight highlight-blue"

    try:
        async with (aiohttp.ClientSession() as session):
            async with session.get(url, params=params, headers=headers) as response:
                page_content = await response.text()

                soup = BeautifulSoup(page_content, 'html.parser')
                silver_prices_data = soup.find_all('div', class_=div_class)[0]
                silver_price = silver_prices_data.find_all('tr')[1]
                silver_price = silver_price.find_all('td')[1].text.replace("KWD", "").strip()

                if silver_price:
                    return float(silver_price), _key, url
                else:
                    print(f'Error fetching data from the website {url}')
                    return None

    except Exception as e:
        print(f'Error fetching data from the website {url} and the error is: {e} ')
        return None


async def get_all_stock_prices(stock_dict):

    stocks_prices = []
    tasks = []
    print()
    start = time.time()

    for key, value in stock_dict.items():
        # URLs represents the urls need to get the price of the stock
        urls = value['urls']
        # _function represents the function need to get the price of the stock
        _function = value['get_price_function']
        for url in urls:
            tasks.append(asyncio.create_task(_function(url, key)))

    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

    for t in done:
        if t.result():
            stock_price = t.result()[0]
            stock_type = t.result()[1]
            stock_url = t.result()[2]
            if stock_price:
                stocks_prices.append((stock_price, stock_type, stock_url))


    end = time.time()
    # get the average price in 3 decimal points
    if stocks_prices:
        return_stock_prices = []
        for key in stock_dict.keys():
            # to handle all gathered prices for each stock type and get the average price for the stock type
            _prices = [(x_stock[0], x_stock[2]) for x_stock in stocks_prices if x_stock[1] == key and x_stock[0]]
            if not _prices:
                print(f'Error fetching data for {key}')
                continue

            stock_average_price = round(sum([x_stock[0] for x_stock in _prices]) / len(_prices), 3)

            max_url_length = max([len(x_stock[1]) for x_stock in _prices])

            for price, url in _prices:
                print(f'The {key} price from website: {url} {" " * (max_url_length - len(url))} is {price} KD')

            return_stock_prices.append((key, stock_average_price))
            print(f'\nThe average {key} price is: {stock_average_price} KD')
            print()

        print(f'\nTime taken: {(end - start):.2f} seconds')
        return return_stock_prices
    else:
        print(f'Error fetching data from the websites')
        return None


def plot_prices(stocks_prices):
    # plot the data in a graph

    stocks_prices_and_dates = []

    if stocks_prices:
        for stock_type, stock_price in stocks_prices:
            try:
                file_name = f'{stock_type.lower()}_prices.json'

                with open(file_name, 'r') as file:
                    stock_data = json.load(file)
                    # Extract dates and prices
                    stock_dates = [datetime.strptime(entry['date'], '%d/%m/%Y %H:%M:%S') for entry in stock_data]
                    stock_prices = [entry['price'] for entry in stock_data]

                    stocks_prices_and_dates.append((stock_type, stock_prices, stock_dates))

            except Exception as e:
                print(f'Error plotting the data: {e}')
    else:
        print(f'Error plotting the data')
        return None

    # Plotting
    plt.figure(figsize=(10, 6))

    for stock_type, stock_prices, stock_dates in stocks_prices_and_dates[:1]:
        plt.plot(stock_dates, stock_prices, marker='o', linestyle='-', label=stock_type, color='gold')

    plt.title('Stocks Prices Over Time')
    plt.xlabel('Date and Time')
    plt.ylabel('Price')
    plt.xticks(rotation=45)

    plt.legend()  # Add legend to distinguish between gold and silver

    # Set the background color to black
    plt.gca().set_facecolor('black')

    plt.tight_layout()
    plt.show()
