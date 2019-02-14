# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 14:50:17 2019

@author: sarge
"""
import sys
import requests
import os

def compDates(a, b):
    #takes in strings of 10-character formatted dates and compares then
    #returns 0 if a and b are the same date
    #returns 1 if a is before b
    #returns 2 if a is after b
    a_year = int(a[0:4])
    a_month = int(a[5:7])
    a_day = int(a[8:10])
    b_year = int(b[0:4])
    b_month = int(b[5:7])
    b_day = int(b[8:10])
    
    if a_year > b_year:
        return 2
    elif a_year < b_year:
        return 1
    else:
        if a_month > b_month:
            return 2
        elif a_month < b_month:
            return 1
        else:
            if a_day > b_day:
                return 2
            elif a_day < b_day:
                return 1
            else:
                return 0


symbol = input("Type the symbol for the stock you want to look up\n")

freq = input("How frequent should data points be? (enter 'day', 'week', or 'month')\n")
freq1 = "invalid"

if freq == "day":
    freq1 = "TIME_SERIES_DAILY"
elif freq == "week":
    freq1 = "TIME_SERIES_WEEKLY"
elif freq == "month":
    freq1 = "TIME_SERIES_MONTHLY"
else:
    print("Invalid frequency specification.\nExiting...")
    sys.exit()

url = "https://www.alphavantage.co/query?function="+freq1+"&symbol="+symbol+"&outputsize=full&apikey=OHSTENF9WCQRB9ES&datatype=csv"
r = requests.get(url)

start_date = input("Type the start date of the data in form: YYYY-MM-DD (don't drop leading zeros)\n")

end_date = input("Type of end data of the data in form: YYYY-MM-DD (don't drop leading zeros)\n")

out_file = "StockData/"+symbol+start_date+freq+end_date+".csv"
temp_out_file = "StockData/"+symbol+start_date+freq+end_date+"TEMP.csv"
with open(temp_out_file, 'wb') as f:  
    f.write(r.content)
    
with open(temp_out_file) as f1, open(out_file, "w") as f2:
    for line in f1:
        if line[0] == "t":
            f2.write(line)
            continue
        elif compDates(line[0:10], start_date) == 2 or compDates(line[0:10], start_date) == 0:
            if compDates(line[0:10], end_date) < 2:
                f2.write(line)
        
os.remove(temp_out_file)
        