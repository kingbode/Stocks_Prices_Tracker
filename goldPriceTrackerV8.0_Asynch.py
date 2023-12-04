"""
in this version:
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

        print()

    else:
        print('Error fetching data from the websites')
        return

    # plot_prices(stocks_prices)


if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
