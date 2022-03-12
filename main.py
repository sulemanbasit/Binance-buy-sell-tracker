#!/usr/bin/env python3

import csv, datetime, calendar, glob, os
import pandas as pd


def import_csv_file():
    """
    Function to get the recent csv file from the root folder where files are usually located and downloaded to
    :return: String of path for the recent csv file to process
    """
    parent_path = r"/Users/sulemanbasit/**"  # ** is to look through all dir/subdir after
    file_type = "/SuB-*.csv"
    file = glob.glob(parent_path+file_type)  # returns a list that matches the pattern
    recent_csv_file = max(file, key= os.path.getctime)  # filters the file with the latest creation time
    return recent_csv_file


def date_range(option):
    """
    Function to return appropriate range of date based on the option chosen by the user
    :param option: Type char of abbreviated option chosen by user
    :return: Appropriate data range of list, sometimes of strings based on the the option
    """
    if option.upper() == "C":
        now_date = datetime.datetime.today().date()
        first_day = now_date.replace(day=1)
        date = pd.date_range(start= str(first_day), end=str(now_date)).to_pydatetime().tolist()
    elif option.upper() == "F":
        any_month_input = input("Input the month number that you want data on, Jan:1 - Dec:12: ")
        year_input = input("input year: ")
        while not year_input.isnumeric():
            year_input = input("input year: ")
        last_day = calendar.monthrange(int(year_input), int(any_month_input))
        date = pd.date_range(start = "2021-{}-01".format(any_month_input), end="2021-{}-{}".format(
            any_month_input,last_day[1])).to_pydatetime().tolist()
    elif option.upper() == "S":
        single_date_input = input("Based on the option chosen, input the date, in yyyy-mm-dd format: ")
        date = single_date_input
    else:
        print("Based on the option chosen,", end=" ")
        start_period = input("input start date, in yyyy-mm-dd format: ")
        end_period = input("input end date, in yyyy-mm-dd format: ")
        date = pd.date_range(start=start_period, end=end_period).to_pydatetime().tolist()
    return date


def normal_csv_read(balance_sheet, date):
    """
    Function that reads a csv file, extracts buy and sell rates of currencies traded according to date and
    returns the list
    :param balance_sheet: Binance CSV file of type Strings
    :param date: Strings of date to extract information for list
    :return: Nested buy and sell list rate of currencies traded
    """
    buy_table = []
    sell_table = []
    for row in balance_sheet:
        order_number, order_type, asset_type, fiat_type, total_price, price, quantity, couterparty, status, created_time = row
        if created_time == "Created Time":
            continue
        created_time_year, created_time_month, created_time_day = date_breakdown(created_time)
        date_year, date_month, date_day = date_breakdown(date)
        # print(type(created_time))
        if date in created_time:
            if status == "Completed":
                if order_type == "Buy":
                    buy_table.append([asset_type, float(price)])
                else:
                    sell_table.append([asset_type, float(price)])
            else:
                continue
        elif created_time_year >= date_year and created_time_month >= date_month and created_time_day > date_day:
            if status == "Completed":
                if order_type == "Buy":
                    buy_table.append([asset_type, float(price)])
                else:
                    sell_table.append([asset_type, float(price)])
            else:
                break
        else:
            continue
    return buy_table, sell_table


def merc_csv_read(merc_sheet, time_period):
    """
    Similar function to normal_csv_read but with more columns
    :param merc_sheet: Binance Merchant CSV file of type Strings
    :param time_period: Strings of date to extract information for list
    :return: Nested buy and sell list rate of currencies traded
    """
    buy_list = []
    sell_list = []
    for row in merc_sheet:
        order_number, advertisement_order_number, order_type, asset_type, fiat_type, quantity_price, price, quantity, \
        exchange_rate, payment_method, counter_party, status, match_time = row
        if status == "Status":
            continue
        match_time_year, match_time_month, match_time_day = date_breakdown(match_time)
        time_period_year, time_period_month, time_period_day = date_breakdown(time_period)
        if time_period in match_time:
            if status == "Completed":
                if order_type == "Buy":
                    buy_list.append([asset_type, float(price)])
                else:
                    sell_list.append([asset_type, float(price)])
            else:
                continue
        elif match_time_year >= time_period_year and match_time_month >= time_period_month and match_time_day > time_period_day:
            if status == "Completed":
                if order_type == "Buy":
                    buy_list.append([asset_type, float(price)])
                else:
                    sell_list.append([asset_type, float(price)])
            else:
                break
        else:
            continue
    return buy_list, sell_list


def date_breakdown(date_time):
    """
    Function to break down string of date to year, month and day
    :param date_time: String of date
    :return: string of year, month and day
    """
    return int(date_time[:4]), int(date_time[5:7]), int(date_time[8:10])


def avg_rate(data_list):
    """
    Function that sums up and averages the rate of same currency. If the currency was not traded within the date range,
    returns 0 for the currency and returns the information in dictionary
    :param data_list: Nested list used to extract average rates of the currency.
    :return: Dictionary of the currency and average rate traded within the date range
    """
    btc_count = 0
    btc_sum = 0
    eth_count = 0
    eth_sum = 0
    bnb_count = 0
    bnb_sum = 0
    usdt_count = 0
    usdt_sum = 0
    for l in data_list: # looping through the list to sum price of appropriate currencies traded
        asset, price = l
        if asset == "BTC":
            btc_count += 1
            btc_sum += price
        elif asset == "ETH":
            eth_count += 1
            eth_sum += price
        elif asset == "BNB":
            bnb_count += 1
            bnb_sum += price
        else:
            usdt_count += 1
            usdt_sum += price
    # check if count is 0, meaning no trades were done
    if btc_count == 0:
        btc_rate = 0.0
    else:
        btc_rate = btc_sum/btc_count
    if bnb_count == 0:
        bnb_rate = 0.0
    else:
        bnb_rate = bnb_sum/bnb_count
    if eth_count == 0:
        eth_rate = 0.0
    else:
        eth_rate = eth_sum/eth_count
    if usdt_count == 0:
        usdt_rate = 0.0
    else:
        usdt_rate = usdt_sum/usdt_count

    return {"BTC": btc_rate, "BNB": bnb_rate, "ETH": eth_rate, "USDT": usdt_rate}


def percent_change(buy_rate, sell_rate):
    """
    Function to find out the % rate of profit margin from the average buy and sell rate
    :param buy_rate: number of type float of the buy rate of the currency
    :param sell_rate: number of type float of the sell of the currency
    :return: % of profit of type float
    """
    return ((sell_rate-buy_rate)/buy_rate)*100



def incomplete_display():
    """
    Function for currency with either no average sell rate and/or average buy rate of the currency, based on the
    choice given
    :return: none
    """
    if option_input == "C":
        print("as of {}:\ncurrency: {}, average buy rate: {}, average sell rate: {}\n".format(date_series[-1], i,
                                                                                              avg_buy[i], avg_sell[i]))
    elif option_input == "F":
        month_num = date_series[0].month
        date_object = datetime.datetime.strptime(str(month_num), "%m")
        full_month_name = date_object.strftime("%B")
        # print(type(full_month_name))
        print("as of {}:\ncurrency: {}, average buy rate: {}, average sell rate: {}\n".format(
            str(full_month_name), i, avg_buy[i], avg_sell[i]))
    elif option_input == "T":
        print("as of {}:\ncurrency: {}, average buy rate: {}, average sell rate: {}\n".format(date_series[-1], i,
                                                                                              avg_buy[i], avg_sell[i]))
    else:
        print("Date: {}\ncurrency: {}, average buy rate: {}, average sell rate: {}\n".format(date_series, i, avg_buy[i],
                                                                                             avg_sell[i]))


# if __name__ == "main":
#     option_input = input("What date range you want to get data on: C: current month till now, F: any full month, "
#                          "S: single date, T: specific time period: ")
#     option_list = ("C", "F", "S", "T")
#     while option_input not in option_list:
#         print("invalid option chosen, try again.")
#         option_input = input("C: current month till now, F: any full month, S: single date, T: specific time period:")
#     recent_file = import_csv_file()
#     print(recent_file)
#     date_series = date_range(option_input)
#     buy_data_list = []
#     sell_data_list = []
#     avg_buy = {}
#     avg_sell = {}
#
#
#     with open(recent_file, 'r') as f:
#         csv_sheet = csv.reader(f)
#         list_csv_sheet = list(csv_sheet)
#         if option_input =="S":
#             if len(list_csv_sheet[0]) == 10:
#                 buy_data, sell_data = normal_csv_read(list_csv_sheet, str(date_series))
#             else:
#                 buy_data, sell_data = merc_csv_read(list_csv_sheet, str(date_series))
#             buy_data_list.extend(buy_data)
#             sell_data_list.extend(sell_data)
#         else:
#             for time in date_series:
#                 if len(list_csv_sheet[0]) == 10:
#                     buy_data, sell_data = normal_csv_read(list_csv_sheet, str(time)[:10])
#                 else:
#                     buy_data, sell_data = merc_csv_read(list_csv_sheet, str(time)[:10])
#                 buy_data_list.extend(buy_data)
#                 sell_data_list.extend(sell_data)
#
#
#     watchlist = ("BTC", "ETH", "BNB", "USDT")
#     if len(buy_data_list) >= 1:
#         avg_buy = avg_rate(buy_data_list)
#     if len(sell_data_list) >= 1:
#         avg_sell = avg_rate(sell_data_list)
#
#     for i in watchlist:
#         if i in avg_buy.keys() and i in avg_sell.keys():
#             # check if both buy and sell rate of the currency is available, otherwise invoke incomplete_display() function
#             if avg_buy[i] > 0 and avg_sell[i] > 0:
#                 percent_rate = percent_change(avg_buy[i], avg_sell[i])
#                 print("{}: {}\n".format(i, percent_rate))
#             else:
#                 incomplete_display()
#         else:
#             # check if currency is in average buy or sell keys
#             if i in avg_buy.keys():
#                 print("currency: {}, average buy rate: {}". format(i, avg_buy[i]))
#             elif i in avg_sell.keys():
#                 print("currency: {}, average buy rate: {}". format(i, avg_sell[i]))
#             else:
#                 print("{} not in data".format(i))
