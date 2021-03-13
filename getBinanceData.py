
def getBinanceData(blockfi_btc, blockfi_eth, plot_portfolio, append_local_csv):
    # Get dependencies
    from binance.client import Client
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    import config
    import csv
    from csv import writer
    
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
    # Get ETH/USD price
    ETH_USD = int(float(client.get_avg_price(symbol='ETHTUSD')['price']))
    
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
    
    
    # labels will be the labels of blockfi + binance assets, labels_alts just binance ones.
    labels = labels_alts
        
    # If BTC isn't already in the binance portfolio insert it to labels and to owned_coins:
    if 'BTC' not in labels:
        labels.insert(0,'BTC')
        owned_coin_BTC_value.insert(0, 0) # later we will sum the actual size 
        
    # If ETH isn't already in the binance portfolio insert it to labels and to owned_coins:
    if 'ETH' not in labels:
        labels.insert(1,'ETH')
        owned_coin_BTC_value.insert(1, 0) # later we will sum the actual size 
        

    # total blockfi ETH in BTC terms:
    blockfi_ETH_BTC_terms = blockfi_eth*price[labels.index('ETH')]
    
    # Total crypto value hedl in portfolio in BTC terms:
    total_value_BTC_terms = total_value_BTC_terms_alts + blockfi_btc + blockfi_ETH_BTC_terms
    
    # Add the ETH & BTC blockfi value in BTC:
    owned_coin_BTC_value[0] = blockfi_btc
    owned_coin_BTC_value[1] = blockfi_ETH_BTC_terms
    
    # get the percentage of each hedl coin:
    percentage = np.multiply(owned_coin_BTC_value, total_value_BTC_terms)
    sizes = np.multiply(percentage, 100)
    
    
    # Get today's date
    today = datetime.today().strftime('%0m/%d/%Y').lstrip("0").replace(" 0", " ")
    
    # Get today's blockfi BTC value in USD
    blockfi_btc_usd = blockfi_btc*BTC_USD
    # Get today's blockfi ETH value in USD
    blockfi_eth_usd = blockfi_eth*ETH_USD
    # Get total binance value in USD
    binance_usd = total_value_BTC_terms_alts*BTC_USD
    
    # Create list ready to be appended in main_balance_&_performance google sheet
    today_data = [
                    today,
                    int(blockfi_btc_usd), 
                    int(blockfi_eth_usd), 
                    'total_blockfi',
                    int(binance_usd),
                    total_value_BTC_terms_alts,
                    'total',
                    'roi15', # will be updated in another function
                    'roi27', # will be updated in another function
                    'roi04', # will be updated in another function
                    BTC_USD,
                    'roi_btc',
                    'btc_distro',
                    'eth_distro',
                    'alts_distro'
                  ]
    
    if append_local_csv:
        # Create array consisting of today's date and today's total alts value in BTC.
        today_row = [datetime.today().strftime('%Y-%m-%d'), total_value_BTC_terms_alts]
        
        # Define the csv file to write/read
        csv_filename = './data/daily_alts_value.csv'
        
        x = []
        # Read daily_alts_value.csv file and assign the first column (dates) to x, and second column (values) to y, excepting the header.
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            if header != None:
                for row in reader:
                    date_time_str = row[0]
                    x.append(date_time_str)
           
        # Define a function to append a row to an existing csv file
        def append_alts_value(file_name, row_to_append):
            with open(file_name, 'a', newline='') as write_obj:
                csv_writer = writer(write_obj)
                csv_writer.writerow(row_to_append)
        
        # If it hasn't been updated today, append today's value:
        if x[len(x)-1] != datetime.today().strftime('%Y-%m-%d'):
            append_alts_value(csv_filename, today_row)
        
    
    if plot_portfolio:
        # Plot the pie charts of portfolio distro
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
        
    
    
    return today_data
    
    


    