#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:15:17 2021

@author: max
"""
def appendToSheet(google_creds_json, today_data):
    # import library to facilitate google sheet API interaction
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    from pprint import pprint
    from datetime import datetime
    
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    
    # Define your credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_creds_json, scope)
    client = gspread.authorize(creds)
    
    # Open your sheet
    sheet = client.open_by_key('1MZaJhVrIG6_3B3AL1wmzn-dX2L7IKzYEmMwuCSwCgC8')
    
    # Define your worksheet
    worksheet = sheet.worksheet('Performance')
    
    
    # function to get next available row
    def next_available_row(worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return len(str_list)+1
    
    # Execute the function to get next_row
    next_row = (next_available_row(worksheet))
    
    # # ROI (13/04/20 - 27/08/20)
    # roi_130420_270820 = 0.2448
    # # ROI (27/08/20 - 15/12/20)
    # roi_270820_151220 = 0.3409
    # # ROI (13/04/20 - 27/08/20)
    # roi_130420_151220 = 0.6692
    
    # total blockfi value
    today_data[3] = '=(INDIRECT((CONCATENATE("B",ROW()))) + INDIRECT((CONCATENATE("C",ROW()))))'
    # total value
    today_data[6] = '=(INDIRECT((CONCATENATE("D",ROW()))) + INDIRECT((CONCATENATE("E",ROW()))))'
    # roi15
    today_data[7] = '''=((INDIRECT((CONCATENATE("G",ROW()))))*'MAIN BALANCE'!$AX$9)/'MAIN BALANCE'!$J$9-1'''
    #roi2708
    today_data[8] = '''='MAIN BALANCE'!$C$20*INDIRECT((CONCATENATE("H",ROW())))+'MAIN BALANCE'!$C$20+INDIRECT((CONCATENATE("H",ROW())))'''
    #roi1304
    today_data[9] = '''='MAIN BALANCE'!$C$21*INDIRECT((CONCATENATE("H",ROW())))+'MAIN BALANCE'!$C$21+INDIRECT((CONCATENATE("H",ROW())))'''
    #btcroi
    today_data[11] = '''=INDIRECT((CONCATENATE("K",ROW())))/19700-1'''
    #btc distro
    today_data[12] = '''=INDIRECT((CONCATENATE("B",ROW())))/INDIRECT((CONCATENATE("G",ROW())))'''
    #eth distro
    today_data[13] = '''=INDIRECT((CONCATENATE("C",ROW())))/INDIRECT((CONCATENATE("G",ROW())))'''
    #alts distro
    today_data[14] = '''=INDIRECT((CONCATENATE("E",ROW())))/INDIRECT((CONCATENATE("G",ROW())))'''
    
    
    # Get today's date
    today = datetime.today().strftime('%m/%d/%Y').lstrip("0").replace(" 0", " ")
    
    # Insert the new row if today's data is not already appended 
    # (use insert_row if you want to choose where to insert it)
    if worksheet.cell(next_row-1,1).value != today:
        worksheet.append_row((today_data), value_input_option="USER_ENTERED")
        # Format the selected columns
        worksheet.format('D', {'textFormat': {'bold': True}})
        worksheet.format('G', {'textFormat': {'bold': True}})
    
