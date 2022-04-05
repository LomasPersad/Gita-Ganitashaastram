#!/usr/bin/python
# -*- coding: utf-8 -*-


# modified from https://www.datacamp.com/community/tutorials/amazon-web-scraping-using-beautifulsoup
# https://bhagavad-gita.org/
# https://jovian.ai/vedant-madane/autosummarize-rulebased
# https://www.youtube.com/watch?v=SWYqp7iY_Tc   Git tutorial
# https://github.com/mpanchmatia/BhagavadGitaAlphabet
# https://github.com/kodematrix/Sentiment-Analysis

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns

#import re
#import time
#from datetime import datetime
#import matplotlib.dates as mdates
#import matplotlib.ticker as ticker
#from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pickle
import json

#testing!!

def get_data( selected_Url,Big_df):
    #Big_df = pd.DataFrame(columns=['Sans','Translit' 'Translation'])

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    r = requests.get(selected_Url, headers=headers)  # , proxies=proxies)
    # r = requests.get(r'https://www.holy-bhagavad-gita.org/chapter/1/verse/'+str(pageNo), headers=headers) #, proxies=proxies)

    content = r.content
    soup = BeautifulSoup(content, features="html.parser")
    # print(soup)

    d = soup.find('div', attrs={'class': 'verseMain'})
    # print(d)
    # get dictionary for sanskrit-meaning
    Sans_meaning = Get_sans_meaning(soup)

    # Get all text, without seperating speaker
    # Verse_san=d.find('div', attrs={'id': 'originalVerse'}).text
    # Transliteration = d.find('div', attrs={'id': 'transliteration'}).text

    Verse_san = d.find('div', attrs={'id': 'originalVerse'})
    # sparse sanskrit verse
    Transliteration = d.find('div', attrs={'id': 'transliteration'})
    # Sparse transliteration
    Speaker, verse_transliteration = get_transliteration(Transliteration)
    sans_Speaker, verse_sans = get_transliteration(Verse_san)

    # Get translation
    # Translation1=soup.select('div#translation')
    # Translation2 = soup.find('div', attrs={'id': 'translation'}).get_text()
    Translation2 = soup.find('div', attrs={'id': 'translation'})
    Translation_text = soup.find('div', attrs={'id': 'translation'}).find_all(text=True)
    # Translation2.find("div",attrs={'class': 'verseShort'}).next_sibling
    final_translation = Translation2.find('span').next_sibling.strip()
    # s2.unwrap()

     # save in dataframe
    Big_df.at['Sans'] = [sans_Speaker+ verse_sans[0]+verse_sans[1]]
    Big_df.at['Translation'] = final_translation
     


    # print(sans_Speaker+ ':\n')
    # print(verse_sans)
    # print(Speaker+ ':\n')
    # print(verse_transliteration)
    # print(final_translation)
    # print(Sans_meaning)

    return Sans_meaning, verse_sans, verse_transliteration, final_translation


def get_transliteration(Transliteration):
    # Transliteration.get_text() #works but text lines lost
    ele = Transliteration.find_all(text=True)  # splits into each part
    del ele[:1]
    del ele[-1:]
    num_ele = len(ele)
    tmp = []  # verse
    sp = []  # speaker

    if ((num_ele - 2) % 2) == 0:
        sp = ''
        for i in range(0, (num_ele - 1)):
            tmp.append(ele[i])
    else:
        sp = ele[0]
        for i in range(1, (num_ele)):
            tmp.append(ele[i])

    return sp, tmp


def Get_sans_meaning(soup):
    """ Original attempt.
    sans_eng=d.find('div', attrs={'id': 'wordMeanings'})
    sans_meaning=sans_eng.find_all(text=True)
    del sans_meaning[:1]
    del sans_meaning[-1:]
    """
    my_dict = {}
    for div in soup.find_all('span', {'class': 'meaning'}):
        # name = div.find('a').text
        name = div.previous_sibling.previous_sibling.text
        value = div.text
        my_dict[name] = value
    return my_dict


def get_urls(url):
    # url_chpt_verse=[]
    url_num = []
    urls = []

    with requests.Session() as session:
        # get all page urls
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        next_link = soup.find_all('span', attrs={'class': 'verseSmall'})
        # d.find('div', attrs={'class': 'verseSmall'})    next_link.find('a')
        for verse_url in soup.find_all('span', attrs={'class': 'verseSmall'}):
            # url_chpt_verse.append(verse_url.find('a')['href'])
            # url_num.append(verse_url.find('a').text)
            # print(verse_url)
            url_num = (verse_url.find('a').text).strip()
            # check url if exist
            url_exist = []
            new_url = url[:-1] + url_num
            urls.append(new_url)

            # check if exist- not necessary
            """
            response = requests.get(new_url)
            if response.status_code == 200:
                print('Page {} exists'.format(url_num))
                urls.append(new_url)
            else:
                print('Web site does not exist for {}'.format(url_num))            
            """
        # print("Processing page: #{page_number}; url: {url}".format(page_number=page_number, url=url))
        return urls


"""
results = []
for i in range(1, no_pages+1):
    results.append(get_data(i))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['Book Name','Author','Rating','Customers_Rated', 'Price'])
df.to_csv('amazon_products.csv', index=False, encoding='utf-8')
"""

# root_url='https://www.holy-bhagavad-gita.org/chapter/1/verse/1'
# get_links(root_url)
# Chapter 1

# base_url='https://www.holy-bhagavad-gita.org/chapter/1/verse/1'
# urls=get_urls(base_url)
# decide to skip this page or not
smallverse = []
Bigdata = []
sanskrit = []
transliteration = []
translation = []

Big_df = pd.DataFrame(columns=['Sans','Translit' 'Translation'])


for i in range(1, 2): #chapters
    base_url = 'https://www.holy-bhagavad-gita.org/chapter/{}/verse/1'.format(str(i))
    print(base_url)
    urls = get_urls(base_url)

    with requests.Session() as session:
        for U in urls: #verses
            response = session.get(U)
            soup = BeautifulSoup(response.content, 'html.parser')
            processed_verse = soup.find('span', attrs={'class': 'verseShort'}).text

            if processed_verse in smallverse:
                print('url already processed: {}'.format(U))
                continue
            else:
                smallverse.append(processed_verse)
                # Sans_meaning = get_data(U)[0]
                Sans_meaning, verse_sans, verse_transliteration, final_translation = get_data(U,Big_df)
                Bigdata.append(Sans_meaning)
                sanskrit.append(verse_sans)
                transliteration.append(verse_transliteration)
                translation.append(final_translation)
                #df.at[U , 'Sans'] = verse_sans
                #df.at[U , 'Translation'] = final_translation


            # print('testing')
            # print(U)

my_json_sans = json.dumps(sanskrit, ensure_ascii=False).encode('utf8')
my_json_translit = json.dumps(transliteration, ensure_ascii=False).encode('utf8')
#print(my_json)

# create a binary pickle file
f = open("meaning.pkl", "wb")
# write the python object (dict) to pickle file
pickle.dump(Bigdata, f, pickle.HIGHEST_PROTOCOL)
# close file
f.close()

f = open("Sans.pkl", "wb")
# write the python object (dict) to pickle file
pickle.dump(my_json_sans, f, pickle.HIGHEST_PROTOCOL)
# close file
f.close()

f = open("transliteration.pkl", "wb")
# write the python object (dict) to pickle file
pickle.dump(my_json_translit, f, pickle.HIGHEST_PROTOCOL)
# close file
f.close()

f = open("translation.pkl", "wb")
# write the python object (dict) to pickle file
pickle.dump(translation, f, pickle.HIGHEST_PROTOCOL)
# close file
f.close()


# Creating the DataFrame
"""
df = pd.DataFrame([sanskrit, transliteration, translation], columns=['Sans', 'Translit', 'Translation'])
# Exporting the DataFrame as csv
df.to_csv('BG.csv', index=False, sep=';')
"""

"""
Bigdata=[]
for i in range(1,4):
 Sans_meaning=get_data(i)[0]
 Bigdata.append(Sans_meaning)
 #print(Sans_meaning)
 #print(i)

print(Bigdata)

"""
