import requests
import csv
from datetime import datetime, timedelta


class CoingeckoAPI:
    basic_url = "https://api.coingecko.com/api/v3"
    coins_list = "/coins/list"
    coins = "/coins"
    history = "/history?"


    def get_coins_list(self):
        url = self.basic_url + self.coins_list
        response = requests.get(url)
        coin_name_list = [d.get("id") for d in response.json()]

        return coin_name_list
    

    def get_coins_history(self,name,date):
        name = "/" + name
        url = self.basic_url +  "/coins" + name + self.history + "date=" + date
        print(url)
        response = requests.get(url)
        # marketcap = response.json().get("market_cap").get("jpy")
        marketcap = response.json().get("market_data")
        if marketcap != None:
            marketcap = marketcap.get("market_cap").get("jpy")

        return marketcap



# 2013 4 28 start
class DayMarketcap:
    total_marketcap = 0
    date_for_print = ""
    date_for_api = ""

    def set_date(self,number):
        date = datetime(2013,4,28,0,0,0) + timedelta(days=number)
        year = date.year
        month = date.month
        day = date.day
        self.date_for_api = str(day) + "-" + str(month) + "-" + str(year)
        self.date_for_print = str(year) + "/" + str(month) + "/" + str(day)

    def add_marketcap(self,marketcap):
        print(marketcap)
        if marketcap != None:
            self.total_marketcap += int(marketcap)

    


def main():
    coingecko = CoingeckoAPI()
    days = []
    coin_name_list = coingecko.get_coins_list()
    print(len(coin_name_list))


    # https://www.nannichime.net/days.php?sy=2013&sm=4&sd=28&ey=2018&em=9&ed=19&f=y
    # 2013.4.28 to 2018.9.19 = 1971 days
    for i in range(100):
        dayMarketcap = DayMarketcap()
        dayMarketcap.set_date(i)
        print(dayMarketcap.date_for_print)

        for name in coin_name_list:
            marketcap = coingecko.get_coins_history(name,dayMarketcap.date_for_api)
            dayMarketcap.add_marketcap(marketcap)

        days.append(dayMarketcap)

    print("Finished getting all data. Printing.")
    
    for day in days:
        print(day.date_for_print　+ " " + day.total_marketcap)

if __name__ == "__main__":
    main()
