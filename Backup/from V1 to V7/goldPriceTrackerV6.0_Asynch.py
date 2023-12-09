"""
in this version:
- we use asyncio to execute the functions concurrently
- we use aiohttp to make the requests to the websites
- we use bs4 to parse the html content
- we collect the gold prices from 4 websites
- we get the average price in 3 decimal points and save it in a json file
- we will plot the data in a graph using matplotlib
- we will add get_silver_price() function to get the silver price from 2 websites
"""

from priceTrackerV6 import *
import asyncio


async def main():

    gold_urls = ['https://pricegold.net/ar/kw-kuwait/',
                 'https://ar.fkjewellers.com/pages/gold-price-in-kuwait',
                 'https://wikigerman.net/gold-kw/',
                 'https://www.livepriceofgold.com/']


    silver_urls = ['https://www.livepriceofgold.com/silver-price/kuwait.html',
                   'https://www.prokerala.com/finance/silver-price.php']

    stocks = {
              'Gold': [gold_urls, get_gold_price24_async],
              'Silver': [silver_urls, get_silver_price_async]
              }

    average_gold_price, average_silver_price = await get_all_stock_prices(stocks)


    if average_gold_price:
        update_gold_price24_json_file(average_gold_price)

    if average_silver_price:
        update_silver_price999_json_file(average_silver_price)

    # plot_prices()


if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
