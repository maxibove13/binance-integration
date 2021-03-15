# Binance Integration

This repo consists of a few scripts that tracks the evolution of our binance account where we hold several altcoins.

### In order to run:

You must have locally a file called `config.py` that contains the Binance `apiKey` & `apiSecurity` taken from your binance account like this:

```
apiKey = <your_key_as_a_string>
apiSecurity = <your_security_key_as_a_string>

Also, a json file containing the google drive & google sheets API credentials is needed.

## List of scripts:

## main.py

Main scripts to run the different functions.
There, as inputs there are the amount of btc and eth hedl in blockfi and the name of the .csv file that contains the total binance value in BTC.

The settings let you choose which plots to run: either the portfolio plot or the alts evolution plot.
Also, you can choose if to append the data to google sheets and to the local csv file (altcoins value)

The script consist of the following functions:

## appendToSheet.py

Function to append data to the google sheet

## altsEvolution.py

Script that reads the .csv file `./data/daily_alts_value.csv` that contains the date and the BTC value of all altcoins held in Binance in that date.
Then that data is plot to know the historical evolution of the altcoins in BTC terms.

## getBinandeData.py

Function that manage binance connection and gives you several data like price of btc, eth, total binance value, value for each coin, etc.

## scheduler.py

File to run main function every day.
