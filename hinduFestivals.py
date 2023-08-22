import requests
import json
from bs4 import BeautifulSoup
from collections import OrderedDict


# print(base_url)


def festivalsLunar():
    # Chaitra (चैत्र) - March/April
    # Vaishakha (वैशाख) - April/May
    # Jyeshtha (ज्येष्ठ) - May/June
    # Ashadha (आषाढ) - June/July
    # Shravana (श्रावण) - July/August
    # Bhadrapada (भाद्रपद) - August/September
    # Ashwin (आश्विन) - September/October
    # Kartika (कार्तिक) - October/November
    # Margashirsha (मार्गशीर्ष) - November/December
    # Pausa (पौष) - December/January
    # Magha (माघ) - January/February
    # Phalguna (फाल्गुन) - February/March

    hindu_months = ['chaitra', 'vaishakha', 'jyeshtha', 'ashadha', 'shravana',
                    'bhadrapada', 'ashwin', 'kartik', 'margashirsha', 'paush', 'magha', 'phalguna']

    festiv = {key: {} for key in hindu_months}

    with requests.Session() as session:
        for m in hindu_months:  # each month
            base_url = 'https://www.drikpanchang.com/festivals/festivals-{}.html'.format(
                m)

            response = session.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            month = soup.find('h2', attrs={'class': 'dpContentTitle'}).text.partition(' ')[
                0].lower()

            uls = soup.find('ol', attrs={'class': 'dpContent'})
            for idx, ul in enumerate(uls):
                newsoup = BeautifulSoup(str(ul), 'html.parser')
                lis = newsoup.find_all('li')
                dict2 = {}
                for li in lis:
                    # print(li.text.split('-'))
                    name = li.text.split('-')[0]
                    descript = li.text.split('-')[1]

                    dict2['name'] = name
                    dict2['descript'] = descript
                    # print(dict2)
                    festiv[month][idx] = dict2

        # print(festiv)

        with open("festivals.json", "w") as outfile:
            json.dump(festiv, outfile)


def festivalsSolar():
    hindu_months = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]

    festiv = {key: {} for key in hindu_months}

    with requests.Session() as session:

        for m in hindu_months:  # each month
            base_url = 'https://www.drikpanchang.com/festivals/month/festivals-{}.html?geoname-id=3573890&year=2023'.format(
                m.lower())
            # print(base_url)

            response = session.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            event_name_divs = soup.find_all(
                'div', attrs={'class': 'dpEventName'})
            # Extract the text content of each div and store in a list
            event_names = [event_name.get_text()
                           for event_name in event_name_divs]
            print(event_names)

        #     uls = soup.find('ol', attrs={'class': 'dpContent'})
        #     for idx, ul in enumerate(uls):
        #         newsoup = BeautifulSoup(str(ul), 'html.parser')
        #         lis = newsoup.find_all('li')
        #         dict2 = {}
        #         for li in lis:
        #             # print(li.text.split('-'))
        #             name = li.text.split('-')[0]
        #             descript = li.text.split('-')[1]

        #             dict2['name'] = name
        #             dict2['descript'] = descript
        #             # print(dict2)
        #             festiv[month][idx] = dict2

        # # print(festiv)

        # with open("festivals.json", "w") as outfile:
        #     json.dump(festiv, outfile)


festivalsSolar()
