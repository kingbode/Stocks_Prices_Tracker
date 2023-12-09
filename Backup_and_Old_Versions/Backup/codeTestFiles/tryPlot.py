import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load JSON data
json_data = '''
[
    {
        "date": "09/10/2023 05:39:02",
        "price": 18.443
    },
    {
        "date": "09/10/2023 05:41:09",
        "price": 18.44275
    },
    {
        "date": "09/10/2023 05:44:01",
        "price": 18.443
    },
    {
        "date": "09/10/2023 05:46:30",
        "price": 18.44375
    }
]
'''

data = json.loads(json_data)

# Extract dates and prices
dates = [datetime.strptime(entry['date'], '%m/%d/%Y %H:%M:%S') for entry in data]
prices = [entry['price'] for entry in data]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(dates, prices, marker='o', linestyle='-', color='b')
plt.title('Gold Prices Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Gold Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
