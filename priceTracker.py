import os
import requests
from bs4 import BeautifulSoup
import convert_numbers
from datetime import datetime
import json

def getGoldPrice24(url):

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if url == 'https://www.livepriceofgold.com/':
            goldPrice24 = soup.find('div', class_="currencyt-h").find_all('table')[1].find_all('tr')[10].find_all('td')[1].text.replace("KWD", "").strip()
        else:
            goldPrice24 = soup.find_all('tbody')[0].find_all('tr')[0].find_all('td')[1].text.replace("د.ك.", "").replace("\xa0\u200f","")

        if url == 'https://wikigerman.net/gold-kw/' or url == 'https://www.livepriceofgold.com/':
            goldPrice24 = float(convert_numbers.hindi_to_english(goldPrice24)) / 100
        else:
            goldPrice24 = float(convert_numbers.hindi_to_english(goldPrice24)) / 1000

        print(f'The gold price from website: {url} {" " * (54 - len(url))} is {goldPrice24} KD')


    except Exception as e:
        print(f'Error fetching data from the website {url}')
        print(e)
        return None

    return goldPrice24


def updateGoldPrice24_JSONFile(averageGoldPrice):
    print('\nUpdating the gold_prices.json file .......', end='')

    if os.path.exists('gold_prices.json'):
        with open('gold_prices.json', 'r') as file:
            data = json.load(file)
            new_update = {
                'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'price': averageGoldPrice
            }

            data.append(new_update)

        with open('gold_prices.json', 'w') as file:
            json.dump(data, file, indent=4)

    else:
        with open('gold_prices.json', 'w') as file:
            new_update = {
                'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'price': averageGoldPrice
            }
            json.dump([new_update], file, indent=4)

    print(' Done')
