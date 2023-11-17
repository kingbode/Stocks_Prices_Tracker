
from priceTracker import *

import asyncio

import time
async def main():

    urls = ['https://pricegold.net/ar/kw-kuwait/',
            'https://ar.fkjewellers.com/pages/gold-price-in-kuwait',
            'https://wikigerman.net/gold-kw/',
            'https://www.livepriceofgold.com/']

    gold_prices = []

    tasks = []

    print()

    start = time.time()

    for url in urls:
        tasks.append( asyncio.create_task(getGoldPrice24_Async(url)) )

    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

    for t, url in zip(done, urls):
        gold_prices.append((t.result(), url))


    end = time.time()

    # get the average price in 3 decimal points
    averageGoldPrice = round(sum([gold_price[0] for gold_price in gold_prices ])/len(gold_prices), 3)

    print(f'\nThe average gold price is: {averageGoldPrice} KD')

    print(f'\nTime taken: {end-start}')

    updateGoldPrice24_JSONFile(averageGoldPrice)


if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())





