
"""
in this version:
- we use asyncio to execute the functions concurrently
- we use aiohttp to make the requests to the websites
- we use bs4 to parse the html content
- we collect the gold prices from 4 websites
- we get the average price in 3 decimal points and save it in a json file
- we will plot the data in a graph using matplotlib
"""

from priceTracker import *
import asyncio


async def main():

    x = update_gold_price24_json_file(1.0)
    print(x)

    urls = ['https://pricegold.net/ar/kw-kuwait/',
            'https://ar.fkjewellers.com/pages/gold-price-in-kuwait',
            'https://wikigerman.net/gold-kw/',
            'https://www.livepriceofgold.com/']

    average_gold_price = await get_all_gold_prices24(urls)

    update_gold_price24_json_file(average_gold_price)

    plot_prices()


if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
