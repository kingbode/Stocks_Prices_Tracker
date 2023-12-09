import requests
from bs4 import BeautifulSoup
import convert_numbers
from datetime import datetime
import aiohttp
import asyncio
import time
import matplotlib.pyplot as plt
import json
import os


def get_gold_price24(url):
    """
    This function takes an url and returns the gold price from that url
    :param url:
    :return: float - the gold price
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if url == 'https://www.livepriceofgold.com/':
            gold_price24 = soup.find('div', class_="currencyt-h").find_all('table')[1]
            gold_price24 = gold_price24.find_all('tr')[10].find_all('td')[1].text.replace("KWD", "").strip()
            gold_price24 = float(convert_numbers.hindi_to_english(gold_price24)) / 100
        else:
            gold_price24 = soup.find_all('tbody')[0].find_all('tr')[0]
            gold_price24 = gold_price24.find_all('td')[1].text.replace("د.ك.", "").replace("\xa0\u200f", "")
            if url == 'https://wikigerman.net/gold-kw/':
                gold_price24 = float(convert_numbers.hindi_to_english(gold_price24)) / 100
            else:
                gold_price24 = float(convert_numbers.hindi_to_english(gold_price24)) / 1000

        print(f'The gold price from website: {url} {" " * (54 - len(url))} is {gold_price24} KD')
        return gold_price24

    except Exception as e:
        print(f'Error fetching data from the website {url} and the error is: {e} ')
        return None


async def get_gold_price24_async(url):
    """
   This function takes an url and returns the gold price from that url
   :param url:
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
                    gold_price24 = float(convert_numbers.hindi_to_english(gold_price24)) / 100
                else:
                    gold_price24 = soup.find_all('tbody')[0].find_all('tr')[0].find_all('td')[1]
                    gold_price24 = gold_price24.text.replace("د.ك.", "").replace("\xa0\u200f", "")
                    if url == 'https://wikigerman.net/gold-kw/':
                        gold_price24 = float(convert_numbers.hindi_to_english(gold_price24)) / 100
                    else:
                        gold_price24 = float(convert_numbers.hindi_to_english(gold_price24)) / 1000

                print(f'The gold price from website: {url} {" " * (54 - len(url))} is {gold_price24} KD')
                return gold_price24

    except Exception as e:
        print(f'Error fetching data from the website {url} and the error is: {e} ')
        return None


async def get_all_gold_prices24(urls):
    gold_prices = []
    tasks = []
    print()
    start = time.time()
    for url in urls:
        tasks.append(asyncio.create_task(get_gold_price24_async(url)))
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    for t, url in zip(done, urls):
        gold_prices.append((t.result(), url))
    end = time.time()
    # get the average price in 3 decimal points
    average_gold_price = round(sum([gold_price[0] for gold_price in gold_prices]) / len(gold_prices), 3)
    print(f'\nThe average gold price is: {average_gold_price} KD')
    print(f'\nTime taken: {end - start}')
    return average_gold_price


def update_gold_price24_json_file(average_gold_price):
    """
    This function takes the average gold price and updates the gold_prices.json file
    :param average_gold_price:
    :return: None
    """
    print('\nUpdating the gold_prices.json file .......', end='')

    if os.path.exists('gold_prices.json'):
        with open('gold_prices.json', 'r') as file:
            data = json.load(file)
            new_update = {
                'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'price': average_gold_price
            }

            data.append(new_update)

        with open('gold_prices.json', 'w') as file:
            json.dump(data, file, indent=4)

    else:
        with open('gold_prices.json', 'w') as file:
            new_update = {
                'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'price': average_gold_price
            }
            json.dump([new_update], file, indent=4)

    print(' Done')


def plot_prices():
    # plot the data in a graph
    try:
        with open('gold_prices.json', 'r') as file:
            data = json.load(file)
            prices = [x['price'] for x in data]
            dates = [x['date'] for x in data]

            plt.plot(dates, prices)

            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.title('Gold Price in Kuwait')
            plt.grid(True)
            plt.savefig('gold_prices.png')
            plt.show()
    except Exception as e:
        print(f'Error plotting the data: {e}')
