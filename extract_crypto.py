# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy import Selector
import csv
import datetime
import requests
import pandas as pd
import json 


def extract(url):
    coins={}
    ticker_symbol={}
    crypto_list={}
    filename = "crypto_records.csv" #csv file in which data will be stored
    j=0
    #retrieve cryptocurrency information from CoinMarketCap
    rawcontent=requests.get(url)
    soupcontent=BeautifulSoup(rawcontent.content,'html.parser')
    if (rawcontent.status_code==200):
        print('Successfully fetched Cryptocurrency data')
    else:
        print(rawcontent.status_code)
    jsondata=soupcontent.find('script',id="__NEXT_DATA__",type="application/json")
    coin_data=json.loads(jsondata.contents[0])
    listings=coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    #make a key value pair for slug and id in a dictionary,use a seperate dictionary to store ticker symbols
    for i in listings:
        coins[str(i['id'])]= i['slug']
        ticker_symbol[str(i['id'])]=i['symbol']
    #create a dictionary using the above dictionaries with key as ticker symbol and currency name as value
    for i in coins:
        crypto_list[ticker_symbol[i]]=coins[i]
    # write the retrieved crypto data into a csv file
    f = open(filename, 'r+')
    f.truncate(0)
    f.close()
    with open(filename,'w') as csv_file:
        fieldnames = ['Name', 'Ticker_Symbol']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for key,value in crypto_list.items():
            writer.writerow({'Name': key, 'Ticker_Symbol': value})
        


    

    
    

def main():
    url = "https://coinmarketcap.com/en/all/views/all/"
    extract(url)


if __name__ == '__main__':
    main()