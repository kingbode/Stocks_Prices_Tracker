
from priceTracker import *

def main():

    urls = ['https://pricegold.net/ar/kw-kuwait/',
            'https://ar.fkjewellers.com/pages/gold-price-in-kuwait',
            'https://wikigerman.net/gold-kw/',
            'https://www.livepriceofgold.com/']

    gold_prices = []

    print()

    for url in urls:
        goldPrice24 = getGoldPrice24(url)
        if goldPrice24:
            gold_prices.append( (goldPrice24,url) )

    # get the average price in 3 decimal points
    averageGoldPrice = round(sum([gold_price[0] for gold_price in gold_prices ])/len(gold_prices), 3)

    print(f'\nThe average gold price is: {averageGoldPrice} KD')

    updateGoldPrice24_JSONFile(averageGoldPrice)


if __name__ == '__main__':
    main()




