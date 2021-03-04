# Get dependencies
from binance.client import Client
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import config
import functools 

# Define the client
client = Client(config.apiKey, config.apiSecurity)


# Get client account info, and get all_assets from that account
info = client.get_account()
all_assets = info['balances']

# Array of all coin symbols and quantities (in that coin terms)
coin_name = []
coin_quant = []
for i in range(len(all_assets)):
    coin_name.append(all_assets[i]['asset'])
    coin_quant.append(float(all_assets[i]['free'])+float(all_assets[i]['locked']))

# Get all coins names and quantities that client owns (i.e. coin_quant > 0.0)
owned_coin_name = []
owned_coin_quant = []
for i in range(len(coin_name)):
    if coin_quant[i] > 0.0:
        owned_coin_name.append(coin_name[i])
        owned_coin_quant.append(coin_quant[i])

# Get price (in BTC) of owned coins
## To get the price of a certain coin given a certain pair, just write symbol="<coin><pair>"

# Create array of coin and pair (BTC)
owned_coin_symbol_pair = []
for i in range(0,len(owned_coin_name)):
    owned_coin_symbol_pair.append(owned_coin_name[i] + 'BTC')

if owned_coin_name[0] == 'BTC':
    owned_coin_symbol_pair.pop(0)
    
# Get price in BTC
price = []
for i in range(len(owned_coin_symbol_pair)):
    price.append(float(client.get_avg_price(symbol=owned_coin_symbol_pair[i])['price'])) 


if owned_coin_name[0] == 'BTC':
    owned_coin_quant.pop(0)     # First item is BTC, it is already in BTC terms.

# Get owned coins value in BTC terms
owned_coin_BTC_value = []
for num1, num2 in zip(owned_coin_quant, price):
    owned_coin_BTC_value.append(num1 * num2)

if owned_coin_name[0] == 'BTC':
    BTC_quant = owned_coin_quant[0]
    owned_coin_BTC_value.insert(0,BTC_quant)


total_value_BTC_terms = np.sum(owned_coin_BTC_value)    # Get the sum of all coins in BTC terms
percentage = np.multiply(owned_coin_BTC_value, total_value_BTC_terms)   # Get the percentage of each coin over the total value

# Plot alts distro
labels = owned_coin_name
sizes = np.multiply(percentage, 100)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# x = []
# y = []
# # Read daily_alts_value.csv file and assign the first column (dates) to x, and second column (values) to y, excepting the header.
# with open(csv_filename, 'r') as file:
#     reader = csv.reader(file)
#     header = next(reader)
#     if header != None:
#         for row in reader:
#             x.append(row[0])
#             y.append(row[1])

# # Plot alts value historical evolution

# plt.plot(x,y)
# plt.grid()
# plt.show()