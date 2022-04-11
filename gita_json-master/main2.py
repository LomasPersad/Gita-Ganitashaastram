#!/usr/bin/python
# -*- coding: utf-8 -*-


# modified from https://www.datacamp.com/community/tutorials/amazon-web-scraping-using-beautifulsoup


import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# import re
# import time
# from datetime import datetime
# import matplotlib.dates as mdates
# import matplotlib.ticker as ticker
# from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
# import pickle
import json
import csv
from Model import Chapter, Verse
import re


data = {}
data["chapters"] = {}
data["verses"] = {}

chapters = data["chapters"]
verses = data["verses"]



def get_data(selected_Url):
    small_df = pd.DataFrame(columns=['Sans', 'Translit' 'Translation'])

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

    Verse_san = d.find('div', attrs={'id': 'originalVerse'}).text
    Transliteration = d.find('div', attrs={'id': 'transliteration'}).text
    Translation2 = soup.find('div', attrs={'id': 'translation'})
    #Translation_text = soup.find('div', attrs={'id': 'translation'}).find_all(text=True)
    final_translation = Translation2.find('span').next_sibling.strip()

    verse = Verse()
    verse.text = Verse_san
    verse.meaning = final_translation
    verse.transliteration = Transliteration
    verse.word_meanings = Sans_meaning
    # verse.verse_number = convertNumberToHindi(verse_number) # uncomment for hindi

    return Sans_meaning, verse

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

def get_chpt_descript():
    # Get chapter descriptions
    with requests.Session() as session:
        response1 = session.get('https://www.holy-bhagavad-gita.org/index')
        soup2 = BeautifulSoup(response1.content, 'html.parser')
        name_list = soup2.find_all(class_='listItem chapterItem')
        name_list_items = []
        for n in name_list:
            name_list_items.append(n.find('p').text.split("-")[-1].strip())

    return name_list_items

def get_chpt_summary():
    #Get Chapter summary
    with requests.Session() as session:
        chapter_sum = {}
        for i in range(1, 19):
            base_url = 'https://www.holy-bhagavad-gita.org/chapter/{}'.format(str(i))
            response1 = session.get(base_url)
            soup2 = BeautifulSoup(response1.content, 'html.parser')
            # name_list = soup2.find_all(class_='chapterIntro')
            name_list = soup2.find('div', attrs={'class': 'chapterIntro'})
            chapter_sum[i] = name_list.text.strip().replace('\xa0',' ')
    return chapter_sum


# root_url='https://www.holy-bhagavad-gita.org/chapter/1/verse/1'
# get_links(root_url)
# Chapter 1

# base_url='https://www.holy-bhagavad-gita.org/chapter/1/verse/1'
# urls=get_urls(base_url)
# decide to skip this page or not
smallverse = []
# meaning = {}
# sanskrit = []
# transliteration = []
# translation = []


name_list_items=get_chpt_descript()
chapter_sum=get_chpt_summary()

#Big_df = pd.DataFrame(columns=['Sans', 'Translit', 'Translation'])
#name_list_items=get_chpt_descript()

with requests.Session() as session:
    chpt=0
    for i in range(1, 19):  # chapters
        base_url = 'https://www.holy-bhagavad-gita.org/chapter/{}/verse/1'.format(str(i))
        # print(base_url)
        urls = get_urls(base_url)

        chapter = Chapter()
        # chapter.chapter_number = hindi_numbers[chapter_number] # uncomment for hindi
        chapter.chapter_number = i  # comment for hindi
        chapter.chapter_summary =chapter_sum[i]
        chapter.name =name_list_items[chpt]
        # chapter.name_meaning = soup.find("h3").text
        # chapter.verse_numbers = []
        verses[i] = {}
        page_no = 1
        for idx, U in enumerate(urls):  # verses
            print(U)
            response = session.get(U)
            soup = BeautifulSoup(response.content, 'html.parser')
            processed_verse = soup.find('span', attrs={'class': 'verseShort'}).text

            if processed_verse in smallverse:
                print('url already processed: {}'.format(U))
                continue
            else:
                smallverse.append(processed_verse)
                Sans_meaning, verse = get_data(U)

                verse.verse_number = page_no  # comment for hindi

                verses[i][str(page_no)] = {}
                verses[i][str(page_no)] = vars(verse)
                page_no += 1

                #save_idx = 'chpt{}V{}'.format(i, idx + 1)
                #meaning[save_idx] = Sans_meaning

        get_chpt=re.findall('\d*\.?\d+', processed_verse)
        num_verse=str(get_chpt[0][-2:])
        chapter.verses_count=num_verse
        #chapter[i]= verses
        #chapters[i] = chapter
        # print('testing')
        # print(U)
        chapters[i] = vars(chapter)
        chpt+= 1


# Writing the data to json file
# Change file name for different language
data_file = open("LP_dataset_english.json", "w", encoding="utf-8")
json.dump(data, data_file, ensure_ascii=False)



