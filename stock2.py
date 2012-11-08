# This is a program that analyzes a .csv file and gives the optimal time to 
# buy and sell a stock based on the past 365 days.
#
# Author: Fanley Tseng

import sys
import datetime

def main():
    price_list=[]   # This stores the items in table.csv into a dictionary.
    # Opens the file.
    infile = open("table.csv")
    # Skips the first line with the titles.
    infile.readline(
)
    # Parses all relevant data into a list. 
    for line in infile:
        price = line.strip().split(",")
        price_list.append({"Date": price[0], "Open": price[1],
                           "High": price[2], "Low": price[3],
                           "Close": price[4], "Volume": price[5],
                           "Adjusted_close": price[6]})

    # Base case if nothing is in the file.
    if len(price_list) == 0:
        print("No values")
        sys.exit()    
    # Otherwise the file is valid for processing.
    else:
        process(price_list)

def process(price_list):
    # Fill the base values.
    low = price_list[0]["Close"]
    low_date = price_list[0]["Date"]
    high = price_list[0]["Close"]
    high_date = price_list[0]["Date"]
    profit = 0

    # Traverse the entire list of prices.
    for i in range(0, len(price_list)):
        if(float(price_list[i]["Close"]) < float(low)):
            low = price_list[i]["Close"]
            low_date = price_list[i]["Date"]
            i += 1
            continue
        elif(float(price_list[i]["Close"]) - float(low) > float(profit)):
            profit = float(price_list[i]["Close"]) - float(low)
            buy_price = low
            buy_date = low_date
            sell_date = price_list[i]["Date"]
            sell_price = price_list[i]["Close"]
            i += 1
            continue
        else:
            i += 1
            continue

    time = calculate_time(buy_date, sell_date)
    print_result(buy_date, buy_price, sell_date, sell_price, profit, time)

# This basically calculates the calendar days between the buy and sell dates.
def calculate_time(buy_date, sell_date):
    buy = buy_date.split("-")
    sell = sell_date.split("-")
    start = datetime.date(int(buy[0]), int(buy[1]), int(buy[2]))
    end = datetime.date(int(sell[0]), int(sell[1]), int(sell[2]))

    # If the day count is negative there is an issue so return -1.
    if (end-start).days < 0:
        return -1
    # Otherwise return the amount of days.
    else:
        return (end-start).days

def print_result(buy_date, buy_price, sell_date, sell_price, profit, time):
    if time == -1:
        print ("Buy date cannot occur before sell date. Please check CSV "
               "file.")
    else:
        print ("Date to buy: %s\nBuy price: $%.2f\nDate to sell: %s\nSell "
               "price: $%.2f\nGains per share: $%.2f\nAmount of time that "
               "the user held the stock: %d days") % (buy_date, 
               float(buy_price), sell_date, float(sell_price), float(profit),
               time)

main()
