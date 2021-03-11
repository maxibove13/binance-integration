# Get dependencies
from binance.client import Client
import numpy as np
import matplotlib.pyplot as plt
import config

# Close all previous figures
plt.close('all')

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
    
# Get BTC/USD price
BTC_USD = int(float(client.get_avg_price(symbol='BTCTUSD')['price']))


# Add BTC price in BTC terms:
if owned_coin_name[0] == 'BTC':
    price.insert(0,1)

# Get owned coins value in BTC terms
owned_coin_BTC_value = []
for num1, num2 in zip(owned_coin_quant, price):
    owned_coin_BTC_value.append(num1 * num2)


total_value_BTC_terms_alts = np.sum(owned_coin_BTC_value)    # Get the sum of all coins in BTC terms
percentage_alts = np.multiply(owned_coin_BTC_value, total_value_BTC_terms_alts)   # Get the percentage of each coin over the total value

# define labels and sizes for alts distro
labels_alts = owned_coin_name
sizes_alts = np.multiply(percentage_alts, 100)


# Add the blockfi assets
labels = labels_alts
    
# If BTC isn't already in the binance portfolio insert it to labels and to owned_coins:
if 'BTC' not in labels:
    labels.insert(0,'BTC')
    owned_coin_BTC_value.insert(0, 0) # later we will sum the actual size 
    
# If ETH isn't already in the binance portfolio insert it to labels and to owned_coins:
if 'ETH' not in labels:
    labels.insert(1,'ETH')
    owned_coin_BTC_value.insert(1, 0) # later we will sum the actual size 
    
# Total BTC & ETH hedl in blockfi:
blockfi_BTC = 1.11549771
blockfi_ETH = 11.39

# total blockfi ETH in BTC terms:
blockfi_ETH_BTC_terms = blockfi_ETH*price[labels.index('ETH')]

# Total crypto value hedl in portfolio in BTC terms:
total_value_BTC_terms = total_value_BTC_terms_alts + blockfi_BTC + blockfi_ETH_BTC_terms

# Add the ETH & BTC blockfi value in BTC:
owned_coin_BTC_value[0] = blockfi_BTC
owned_coin_BTC_value[1] = blockfi_ETH_BTC_terms

# get the percentage of each hedl coin:
percentage = np.multiply(owned_coin_BTC_value, total_value_BTC_terms)
sizes = np.multiply(percentage, 100)



    

# Plot the pie charts

fig, axs = plt.subplots(1, 2) # define the plot

# set the first subplot (total distro)
axs[0].pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
axs[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
axs[0].set_title('Portfolio distribution')

# set the second subplot (alts distro)
axs[1].pie(sizes_alts, labels=labels_alts, autopct='%1.1f%%',
        shadow=False, startangle=90)
axs[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
axs[1].set_title('Altcoins distribution')

fig.suptitle(f'Currently HODLing: %1.4f BTC \n @ {BTC_USD} BTC/USD' %total_value_BTC_terms, fontsize=16)
plt.show()