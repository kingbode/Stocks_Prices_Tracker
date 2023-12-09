"""
in this version:
- made the stocks data read from the stocks.json file, to make the code more generic
"""
import sys

from priceTrackerV9 import *
import asyncio


async def main():
    # read the stocks dict from the stocks.json file
    stocks_data = get_stocks_data()

    if not stocks_data:
        return return_codes['stocks.json file not found']

    print()
    # add progress bar using tqdm
    await progress_bar()

    # get uptodate prices for all stocks
    stocks_prices = await get_all_stock_prices(stocks_data)

    # update the json file with the uptodate prices
    if stocks_prices:
        update_stock_price_json_file(stocks_data, stocks_prices)

        print()
        return return_codes['Success']

    else:
        print('Error fetching data from the websites')
        return return_codes['Error fetching data from the websites']

    # plot_prices(stocks_prices)





if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(main())

    # print(result)
    sys.exit(result)

