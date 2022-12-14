import time
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types

from urllib import request
import json

import datetime

TOKEN = ""
MSG = "Хотите узнать погоду?"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    text = message.text
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    await message.reply(f"Привет, {user_full_name}!")
    await message.reply(f"Чтобы открыть список команд напишите /help")

    for i in range(7):
        await asyncio.sleep(60 * 60 * 24)
        await bot.send_message(user_id, MSG.format(user_name))


@dp.message_handler(commands=['send_some_cutie'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    text = message.text
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    await message.reply(f"""Увидеть котика: /cat 
Увидеть пёсика: /dog""")

@dp.message_handler(commands=['cat'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    text = message.text
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    s = 'https://api.thecatapi.com/v1/images/search'
    s = request.urlopen(s).read()
    data = json.loads(s)

    await message.reply(data[0]['url'])


@dp.message_handler(commands=['dog'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    text = message.text
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')


    s = 'https://api.thedogapi.com/v1/images/search'
    s = request.urlopen(s).read()
    data = json.loads(s)

    await message.reply(data[0]['url'])

@dp.message_handler(commands=['weather_now'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    text = message.text

    city_name = message.text.split()

    if len(city_name) == 2:
        city_name = city_name[-1]
    else:
        city_name = '+'.join(city_name[1:])

    if message.text == 'weather_now':
        city_name = 'Moscow'

    s = (request.
         urlopen(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&lat=55.751244&lon=37.618423&units=metric&appid=db2c25ac814dee393298a0215779ad04')
         .read())
    data = json.loads(s)

    weather = data['weather'][0]['description']

    temperature = round(data['main']['temp'], 2)
    feels_like = round(data['main']['feels_like'], 2)

    pressure = data['main']['pressure']
    pressure *= 0.7501
    pressure = round(pressure, 2)
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    timezone = data['timezone']
    sunrise = datetime.datetime.utcfromtimestamp(sunrise + timezone).strftime('%H:%M:%S')
    sunset = datetime.datetime.utcfromtimestamp(sunset + timezone).strftime('%H:%M:%S')

    degree_sign = u'\N{DEGREE SIGN}'

    city_name_for_msg = data['name']

    await message.reply(f"""Погода для города: {city_name_for_msg}

Погода/осадки: {weather}

Температура: {temperature} {degree_sign}C
Ощущается как: {feels_like} {degree_sign}C

Давление: {pressure}мм рт. ст.
Влажность: {humidity}%
Скорость ветра: {wind_speed} м/с

Время восхода: {sunrise}
Время заката: {sunset}""")

@dp.message_handler(commands=['weather_5_days'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    text = message.text

    city_name = message.text.split()

    if len(city_name) == 2:
        city_name = city_name[-1]
    else:
        city_name = '+'.join(city_name[1:])

    if text == 'weather_5_days':
        city_name = 'Moscow'

    try:
        s = (request.
             urlopen(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid=db2c25ac814dee393298a0215779ad04')
             .read())
        data = json.loads(s)
    except:
        s = (request.
             urlopen(
            f'https://api.openweathermap.org/data/2.5/forecast?q=Moscow&units=metric&appid=db2c25ac814dee393298a0215779ad04')
             .read())
        data = json.loads(s)

    today = datetime.datetime.utcfromtimestamp(data['list'][0]['dt'] + data['city']['timezone']).strftime(
        '%d.%m.%Y %H:%M:%S')
    today = today.split()[0].strip()
    today_str = ''
    days_dic = {}
    degree_sign = u'\N{DEGREE SIGN}'

    for i in range(40):
        date_time = datetime.datetime.utcfromtimestamp(data['list'][i]['dt'] + data['city']['timezone']).strftime(
            '%d.%m.%Y %H:%M:%S')
        temperature = data['list'][i]['main']['temp']
        weather = data['list'][i]['weather'][0]['description']

        if today in date_time:
            if len(today_str) == 0:
                today_str += today + '\n'
            today_str += f'''{date_time.split(today)[1].strip()}, {temperature}{degree_sign}C, {weather}\n'''
        else:
            if '00:00:00' in date_time:
                date = date_time.split('00:00:00')[0].strip()
                days_dic[date] = f'Ночь: {temperature}{degree_sign}C, {weather}\n'
            if '01:00:00' in date_time:
                date = date_time.split('01:00:00')[0].strip()
                days_dic[date] = f'Ночь: {temperature}{degree_sign}C, {weather}\n'
            if '02:00:00' in date_time:
                date = date_time.split('02:00:00')[0].strip()
                days_dic[date] = f'Ночь: {temperature}{degree_sign}C, {weather}\n'
            if '12:00:00' in date_time:
                date = date_time.split('12:00:00')[0].strip()
                days_dic[date] += f'День: {temperature}{degree_sign}C, {weather}\n'
            if '13:00:00' in date_time:
                date = date_time.split('13:00:00')[0].strip()
                days_dic[date] += f'День: {temperature}{degree_sign}C, {weather}\n'
            if '14:00:00' in date_time:
                date = date_time.split('14:00:00')[0].strip()
                days_dic[date] += f'День: {temperature}{degree_sign}C, {weather}\n'

    days_str = ''

    for k, v in days_dic.items():
        days_str += k + '\n' + v + '\n'

    city_name_for_msg = data['city']['name']
    weather = f'Почасовая погода в {city_name_for_msg} на сегодня: ' + today_str + '\nПогода на следующие 5 дней\n\n' + days_str

    await message.reply(weather)


@dp.message_handler(commands=['help'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    text = message.text

    await message.reply(f"""1. Погода сейчас:
/weather_now [название города на английском языке],
например, /weather_now Moscow

2. Погода на 5 дней:
/weather_5_days [название города на английском языке],
например, /weather_5_days Moscow

3. Если вас расстроила погода:
/send_some_cutie""")


if __name__ == '__main__':
    executor.start_polling(dp)

