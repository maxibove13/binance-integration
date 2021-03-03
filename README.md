# Binance Integration

This repo consists of a few scripts that tracks the evolution of our binance account where we hold several altcoins.

### In order to run:

You must have locally a file called `config.py` that contains the Binance `apiKey` & `apiSecurity` taken from your binance account like this:

```
apiKey = <your_key_as_a_string>
apiSecurity = <your_security_key_as_a_string>
```

## List of scripts:

## getAltsPortfolio.py

Script that reads binance balance account, takes all the owned coin with a quantity greater than 0 and plot them in a pie chart to know the current altcoins distribution.

## altsEvolution.py

Script that reads the .csv file `./data/daily_alts_value.csv` that contains the date and the BTC value of all altcoins held in Binance in that date.
Then that data is plot to know the historical evolution of the altcoins in BTC terms.

## appendAltsEvolutionData.py

Script that gets the total BTC value of all altcoins held in Binance as of today and appends the current data with the corresponding date to the file `./data/daily_alts_value.csv`
