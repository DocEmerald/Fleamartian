import os
import discord
from bs4 import BeautifulSoup
import requests, json, lxml
from re import sub
from decimal import Decimal
import math
import io
import itertools
import csv
import pandas
import re
import statistics
import random
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
TOKEN = ('')
GUILD = ('')
global average
global search
class discrs():
    def get_results():
        global search
        searchurl = (('https://www.ebay.com/sch/i.html?_nkw=') + search)
        html = requests.get('https://www.ebay.com/sch/i.html?_nkw='+ (search), headers=headers).text
        soup = BeautifulSoup(html, 'lxml')

        data = []

        for item in soup.select('.s-item__wrapper.clearfix'):
            title = item.select_one('.s-item__title').text
            link = item.select_one('.s-item__link')['href']
        
            try:
                condition = item.select_one('.SECONDARY_INFO').text
            except:
                condition = None

            try:
                shipping = item.select_one('.s-item__logisticsCost').text
            except:
                shipping = None

            try:
                location = item.select_one('.s-item__itemLocation').text
            except:
                location = None

            try:
                watchers_sold = item.select_one('.NEGATIVE').text
            except:
                watchers_sold = None

            if item.select_one('.s-item__etrs-badge-seller') is not None:
                top_rated = True
            else:
                top_rated = False

            try:
                bid_count = item.select_one('.s-item__bidCount').text
            except:
                bid_count = None

            try:
                bid_time_left = item.select_one('.s-item__time-left').text
            except:
                bid_time_left = None

            try:
                reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
            except:
                reviews = None

            try:
                exctention_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
            except:
                exctention_buy_now = None

            try:
                price = item.select_one('.s-item__price').text.split()
                                                                 
            except:
                price = None
            page = requests.get(searchurl)
            soup=BeautifulSoup(page.text, 'lxml')
            sep = (' ')
            sep2 = ('T')
            sep3 = ("'")
            data = []
            for item in soup.select('.s-item__wrapper'):
                data.append(
                    (item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',','').split(sep, 1)[0].split(sep2,1)[0]))
            for i in data:
                if(len(i)==0):
                    data.remove(i)
                
            print(data)
            a = [float(i) for i in data]
            print(a)
            sumprice = (sum(a))
            length = (len(a))
            global average
            average = (sumprice/length)
            i = 0
            while i == 0:
                print("The average price of " + (search) + " is $" + (str(average)))
                i = 1
            else:
                print("____________________________________________________")
                break
            data.append({
                'item': {'title': title, 'link': link, 'price': price},
                'condition': condition,
                'top_rated': top_rated,
                'reviews': reviews,
                'watchers_or_sold': watchers_sold,
                'buy_now_extention': exctention_buy_now,
                'delivery': {'shipping': shipping, 'location': location},
                'bids': {'count': bid_count, 'time_left': bid_time_left},
            })

        #print(json.dumps(data, indent = 2, ensure_ascii = False))
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        f.close()



client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
global search
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    initmessage = ("Initialization in progress, standby...")

    if message.content == '!scraper':
        channel = message.channel
        response = (initmessage)
        await message.channel.send(response)
        await message.channel.send("Enter your search keyword below. Be as accurate and specific as possible.")
        def check(message1):
            global search
            global average
            
            search = message1.content
            discrs.get_results()
            return message.author == message1.author
        global average
        global search
        msg = await client.wait_for('message', check=check)
        await channel.send(("The average price of " + (search) + " is $" + (str(average))))
        
        
client.run(TOKEN)
                

