
import pandas as pd
import lxml


from googletrans import Translator
translator = Translator()
import openpyxl
import requests
from bs4 import BeautifulSoup as bs




world = pd.read_excel('worldcities.xlsx')
world = world.drop(['city_ascii', 'country', 'iso2', 'iso3', 'admin_name', 'capital', 'population', 'id'], axis=1)
world = world.drop_duplicates(subset='city')
print(world)


locs_ru = pd.read_excel('spisok_gorodov_RU.xlsx')
locs = locs_ru.drop(['Регион', 'Округ'], axis=1)
print(locs)

def weather(city):
    if locs['Название города'].isin([city]).any() == False:
        result = translator.translate(text=city, src='ru', dest='en')
        city = result.text
        print(city)
        lat = world[world['city'] == city].iloc[0]["lat"]
        lon = world[world['city'] == city].iloc[0]["lng"]
        print(lat, lon)
    else:
        lat = locs[locs['Название города'] == city].iloc[0]["Широта"]
        lon = locs[locs['Название города'] == city].iloc[0]["Долгота"]
        print(lat, lon)


    url = "https://yandex.com.am/weather/?lat=" + str(lat) + "&lon=" + str(lon)
    r = requests.get(url)
    #print(r, url)

    soup = bs(r.text, "lxml")
    #print(soup)

    temp = soup.find_all('span', 'temp__value temp__value_with-unit')
    print(temp[1].text)

