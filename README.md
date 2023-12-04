# GoldPriceTracker
Scraping and Tracking Gold Prices using Python

## Description
This tools is intended t show how to scrape information from multiple websites and track the price of gold.
The tool will scrape the price of gold from multiple websites and store the information in a JSON file.
The tool will also display the price of gold in a graph across the time, and intended at the end to be run as a cron job to track the price of gold.
Could be installed on a Raspberry Pi and connected to a screen to display the price of gold.
or could be installed on a server and send the information to a website, or to a mobile app.


## Videos to explain the code
https://www.youtube.com/watch?v=ijY9xcsvReM&list=PLgG8HRRNnCqwKU1RQHtcnMoUlva7SEy0E

### References
reference for Python Asynchronous Programming
https://www.youtube.com/watch?v=cZ3iHLIDzVI&list=PLhTjy8cBISEpfMihZ8E5yynf5sqPCcBXD&index=1&t=0s

### in version goldPriceTrackerV1.0.py
- use bs4 to parse the html content
- collect the gold prices from 4 websites
- get the average price in 3 decimal points and save it in a json file
- created a functions library "priceTracker.py" file that contains all the functions ( get_gold_price24 , update_gold_price24_json_file )

### in version goldPriceTrackerV2.0_Async.py
- use asyncio to execute the functions concurrently
- use aiohttp to make the requests to the websites
- use bs4 to parse the html content
- collect the gold prices from 4 websites
- get the average price in 3 decimal points and save it in a json file
- updated the functions library "priceTracker.py" with functions ( get_gold_price24 , update_gold_price24_json_file , get_gold_price24_async)


### in version goldPriceTrackerV3.0_Async.py
- plot the data in a graph using matplotlib
- added more refactoring to the code
- updated the functions library "priceTracker.py" with functions:
   get_gold_price24 ,
   update_gold_price24_json_file , 
   get_gold_price24_async ,
   get_all_gold_prices24 , 
   plot_gold_prices24

### in version goldPriceTrackerV4.0_Async.py
- added more refactoring to the code
- updated the functions library "priceTracker.py" with functions:
   get_silver_price ,
   get_silver_price_async ,
   get_all_silver_prices999 ,

### in version goldPriceTrackerV6.0_Async.py
- added more refactoring to the code
- we made a single function to get the prices of gold and silver, and we named it get_all_stock_prices
- updated the functions library "priceTrackerV6.py" with functions:
   get_gold_price24_async ,
   update_gold_price24_json_file ,
   get_silver_price_async ,
   update_silver_price999_json_file ,
   get_all_stock_prices ,
   plot_prices ,

### in version goldPriceTrackerV7.0_Async.py
- added more refactoring to the code
- updated the functions library "priceTrackerV7.py" with functions:

   get_gold_price24_async ,
   get_silver_price_async ,
   update_stock_price_json_file ,
   get_all_stock_prices ,
   plot_prices ,

### in version goldPriceTrackerV8.0_Async.py
- added stocks.json file to store the stocks symbols and names and functions
- updated the functions library "priceTrackerV8.py" with functions:
    
   updated the function "update_stock_price_json_file" to show the stock price status (up or down) and the percentage of change

