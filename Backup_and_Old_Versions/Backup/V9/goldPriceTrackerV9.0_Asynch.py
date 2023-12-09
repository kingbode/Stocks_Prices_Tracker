"""
in this version:
- made the stocks data read from the stocks.json file, to make the code more generic
"""
from tqdm import tqdm

from priceTrackerV9 import *
import asyncio


async def main():
    # read the stocks dict from the stocks.json file
    stocks_data = get_stocks_data()

    if not stocks_data:
        return

    print()
    # add progress bar using tqdm
    tdqm_message = 'Fetching stocks prices from the websites'
    with tqdm(total=100, desc=tdqm_message,
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} {postfix}') as pbar:
        for i in range(8):
            await asyncio.sleep(0.45)
            pbar.update(12.5)

    # get uptodate prices for all stocks
    stocks_prices = await get_all_stock_prices(stocks_data)

    # update the json file with the uptodate prices
    if stocks_prices:
        update_stock_price_json_file(stocks_data, stocks_prices)

        print()

    else:
        print('Error fetching data from the websites')
        return

    # plot_prices(stocks_prices)


if __name__ == '__main__':

    # to fix a known bug in that return error on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
