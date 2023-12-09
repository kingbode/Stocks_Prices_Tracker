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

from priceTrackerV8 import *
import asyncio


def get_stocks_dict():
    # read the stocks dict from the stocks.json file
    try:
        with open('stocks.json', 'r') as f:
            stocks = json.load(f)
        return stocks
    except FileNotFoundError:
        print('stocks.json file not found')
        return None


async def main():

    # stocks = {
    #           'Gold': {
    #               'URLs':['https://pricegold.net/ar/kw-kuwait/',
    #              'https://ar.fkjewellers.com/pages/gold-price-in-kuwait',
    #              'https://wikigerman.net/gold-kw/',
    #              'https://www.livepriceofgold.com/'],
    #
    #               'get_price_function':'get_gold_price24_async'
    #           },
    #           'Silver': {
    #               'URLs': ['https://www.livepriceofgold.com/silver-price/kuwait.html',
    #                'https://www.prokerala.com/finance/silver-price.php'],
    #
    #               'get_price_function': 'get_silver_price_async'
    #               }
    #           }
    #
    # # save the stocks dict in a json file
    # with open('stocks.json', 'w') as f:
    #     json.dump(stocks, f, indent=4)

    stocks = get_stocks_dict()
    # update the get price function for each stock by the actual function from the priceTrackerV8.py file
    for stock_type, stock_data in stocks.items():
        stock_data['get_price_function'] = eval(stock_data['get_price_function'])
    if not stocks:
        return -1



    stocks_prices = await get_all_stock_prices(stocks)

    if stocks_prices:
        for stock_type, stock_price in stocks_prices:
            update_stock_price_json_file(stock_type, stock_price)

    # plot_prices(stocks_prices)


if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
