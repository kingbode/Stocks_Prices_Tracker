
from priceTracker import *

import time

def main():

    urls = ['https://pricegold.net/ar/kw-kuwait/',
            'https://ar.fkjewellers.com/pages/gold-price-in-kuwait',
            'https://wikigerman.net/gold-kw/',
            'https://www.livepriceofgold.com/']

    gold_prices = []

    print()

    start = time.time()

    for url in urls:
        goldPrice24 = get_gold_price24(url)
        if goldPrice24:
            gold_prices.append( (goldPrice24,url) )

    end = time.time()

    # get the average price in 3 decimal points
    averageGoldPrice = round(sum([gold_price[0] for gold_price in gold_prices ])/len(gold_prices), 3)

    print(f'\nThe average gold price is: {averageGoldPrice} KD')

    print(f'\nTime taken: {end-start}')

    update_gold_price24_json_file(averageGoldPrice)


if __name__ == '__main__':
    main()




