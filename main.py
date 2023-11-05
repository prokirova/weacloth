from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import openpyxl
import requests
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('page.html')

def get_weather(city):
    city = GoogleTranslator(source='ru').translate(city)

    appid = 'f5065d392d376613116f54213d16a468'
    res = requests.get(
        "http://api.openweathermap.org/data/2.5/find?q=" + city + "&type=like&units=metric&APPID=" + appid)

    data = res.json()
    sky = data['list'][0]['weather'][0]['description']

    temp = round(float(data['list'][0]['main']['temp']))
    feels_temp = round(float(data['list'][0]['main']['feels_like']))

    return temp, feels_temp, sky

def prediction(temp):
    clothes_base = pd.read_excel(os.getcwd().replace('venv', '') + "clothes_base (4).xlsx")
    clothes = clothes_base[clothes_base['weather'] == temp]

    clothes = clothes.drop(['weather'], axis=1).to_dict(orient='list')
    outerwear = ''.join(map(str, clothes['outerwear']))
    top = ''.join(map(str, clothes['top']))
    bottom = ''.join(map(str, clothes['bottom']))
    feet = ''.join(map(str, clothes['feet']))
    return outerwear, top, bottom, feet


def icon(weather):
    base = ['sun', 'rain', 'clouds', 'thunder', 'snow', 'sky']
    sky = weather.split()
    if sky[-1] in base:
        if sky[-1] == 'sky':
            return 'sun.png'
        return sky[-1] + '.png'
    else:
        return 'icon.png'


@app.route('/clothes', methods=['POST'])
def clothes():
    if request.method == 'POST':
        city = request.form['city']

        temp, feels_temp, sky = get_weather(city)
        city = GoogleTranslator(target='ru').translate(city)
        city = city.capitalize()
        way = []
        if temp <= 0 and temp > -10:
            way.append('notsocold1.jpg')
            way.append('notsocold2.jpg')
            way.append('notsocold3.jpg')
        elif temp > -20 and feels_temp <= -10:
            way.append('middlecold1.jpg')
            way.append('middlecold2.jpg')
            way.append('middlecold3.jpg')
            
        elif temp <= -20:
            way.append('cold1.jpg')
            way.append('cold2.jpg')
            way.append('cold3.jpg')
        elif temp > 0 and temp <= 10 :
            way.append('notsohot1.jpg')
            way.append('notsohot2.jpg')
            way.append('notsohot3.jpg')
        elif temp > 10 and temp <= 20 :
            way.append('middlehot1.jpg')
            way.append('middlehot2.jpg')
            way.append('middlehot3.jpg')
        elif temp > 20:
            way.append('hot1.jpg')
            way.append('hot2.jpg')
            way.append('hot3.jpg')


        outerwear, top, bottom, feet = prediction(temp)
        if feels_temp > 0:
            feels_temp = "+" + str(feels_temp)
        if temp > 0:
            temp = "+ " + str(temp)

        return render_template('clothes.html', city=city, weather=temp, outerwear=outerwear, top=top,
                               bottom=bottom, feet=feet, feels=feels_temp, way=way, sky=icon(sky))
    else:
        pass


if __name__ == '__main__':
    app.run()
