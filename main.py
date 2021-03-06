#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 19:20:32 2021

@author: max
"""

def main():
    from getBinanceData import getBinanceData
    from appendToSheet import appendToSheet
    from altsEvolution import altsEvolution

    # INPUTS
    btc_blockfi = 1.11549771
    eth_blockfi = 11.39
    csv_filename_alts_evol = './data/daily_alts_value.csv'

    # SETTINGS  
    plot_portfolio = 0      # Select whether to plot portfolio or not
    plot_alts_evol = 0      # Plot alts evolution in BTC
    append_data = 1         # Select whether to append data to sheet or not
    append_local_csv = 0    # Select whether to append total BTC value in binance to local .csv file

    # Get blockfi_btc_usd, blockfi_eth_usd, binance_usd, btc_usd
    # blockfi_btc & blockfi_eth as args
    today_data = getBinanceData(btc_blockfi, eth_blockfi, plot_portfolio, append_local_csv)

    # Append that data to the main_balance_&_performance google sheet
    if append_data:
        appendToSheet("crypto-analysis-1758b81dfe9b.json", today_data)
        
    if plot_alts_evol:
        altsEvolution(csv_filename_alts_evol)

main()
    
