# This is a program that analyzes a .csv file and gives the optimal time to 
# buy and sell a stock based on the past 365 days.
#
# Author: Fanley Tseng

import sys
import datetime

def main():
    price_list = []   # Stores the prices from the table.csv file.
    result_list = []  # Stores the chunks of profit regions.
    # Opens the file.
    infile = open("./table.csv")
    # Skips the first line with the titles.
    infile.readline()

    # Parses all relevant data into a list. 
    for line in infile:
        price = line.strip().split(",")
        price_list.append({"Date": price[0], "Open": price[1],
                           "High": price[2], "Low": price[3],
                           "Close": price[4], "Volume": price[5],
                           "Adjusted_close": price[6]})
    # Base case if there is nothing in ./table.csv
    if len(price_list) == 0:
        print("No values in ./table.csv")
        sys.exit()

    process(price_list, result_list)
    find_max(result_list)

# This method will process the list of prices so each profit region is
# broken up into small chunks of profit regions. All regions where profit
# is greater than or equal to zero are recorded.
def process(price_list, result_list):
    count = -1

    for price in price_list:
        # Base case for the first profit region
        if count == -1:
            result_list.append({"Low": price["Close"],
                                "Low_date": price["Date"],
                                "High": price["Close"],
                                "High_date": price["Date"],
                                "Profit": 0})
            count = 0
            result_list[0]["High"] = price["Close"]
            result_list[0]["Low"] = price["Close"]
            continue
        # Check to see if the new price is higher than the oldest high. If so
        # replace the old max with this one.
        elif result_list[count]["High"] < price["Close"]:
            result_list[count]["High"] = price["Close"]
            result_list[count]["High_date"] = price["Date"]
            result_list[count]["Profit"] = (float(result_list[count]["High"]) 
                                            -float(result_list[count]["Low"]))
            continue
        # If the new price is a new low, create a new profit region.
        elif result_list[count]["Low"] > price["Close"]:
            result_list.append({"Low": price["Close"],
                                "Low_date": price["Date"],
                                "High": price["Close"],
                                "High_date": price["Date"],
                                "Profit": 0})
            count += 1
            continue
        # Default in case the price is not higher than high nor lower than low.
        # Could happen if all prices on the table are identical.
        else:
            continue

# Since only one buy and one sell can occur, this method finds the absolute 
# best time to buy and sell assuming you only get to buy and sell once.
def find_max(result_list):
    profit = 0

    for result in result_list:
        if profit < result["Profit"]:
            buy_price = result["Low"]
            buy_date = result["Low_date"]
            sell_price = result["High"]
            sell_date = result["High_date"]
            profit = result["Profit"]
            continue
        else:
            continue

    time = calculate_time(buy_date, sell_date)
    print_result(buy_date, buy_price, sell_date, sell_price, profit, time)

# This basically calculates the calendar days between the buy and sell dates.
def calculate_time(buy_date, sell_date):
    buy = buy_date.split("-")
    sell = sell_date.split("-")
    # Puts the date into an actual date object.
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
