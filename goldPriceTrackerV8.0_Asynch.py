"""
in this version:
- we use asyncio to execute the functions concurrently
- we use aiohttp to make the requests to the websites
- we use bs4 to parse the html content
- we collect the gold prices from 4 websites
- we get the average price in 3 decimal points and save it in a json file
- we will plot the data in a graph using matplotlib
- we will add get_silver_price() function to get the silver price from 2 websites
- made the stocks data read from the stocks.json file, to make the code more generic
"""

from priceTrackerV8 import *
import asyncio


async def main():
   
    stocks = get_stocks_data()

    if not stocks:
        return
   
    stocks_prices = await get_all_stock_prices(stocks)

    if stocks_prices:
        for stock_type, stock_price in stocks_prices:
            update_stock_price_json_file(stock_type, stock_price)

    # plot_prices(stocks_prices)


if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
