'''
A desktop application that displays current weather data by the name of the city.
Information via API from the service https://openweathermap.org/
'''

from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import requests
import time

try:
    import settings
except ImportError:
    exit('Do copy settings.py.default settings.py and set api_key')


def get_weather(event=''):
    if not entry.get():
        messagebox.showwarning('Warning', 'Введите запрос в формате city, country_code')
    else:
        params = {
            'appid': settings.API_KEY,
            'q': entry.get(),
            'units': 'metric',
            'lang': 'ru'
        }
        r = requests.get(settings.API_URL, params=params)
        # https://api.openweathermap.org/data/2.5/weather?appid=key&q=kiev,ua
        weather = r.json()
        label['text'] = print_weather(weather)


def print_weather(weather):
    try:
        city = weather['name']
        country = weather['sys']['country']
        temp = weather['main']['temp']
        press = weather['main']['pressure']
        humidity = weather['main']['humidity']
        wind = weather['wind']['speed']
        desc = weather['weather'][0]['description']
        sunrise_ts = weather['sys']['sunrise']
        sunset_ts = weather['sys']['sunset']
        sunrise_struct_time = time.localtime(sunrise_ts)
        sunset_struct_time = time.localtime(sunset_ts)
        sunrise = time.strftime("%H:%M:%S", sunrise_struct_time)
        sunset = time.strftime("%H:%M:%S", sunset_struct_time)
        return f'Текущие данные о погоде\n' \
               f'Местоположение: {city}, {country} \nТемпература: {temp} °C \nАтм. давление: {press} гПа \n' \
               f'Влажность: {humidity}% \nСкорость ветра: {wind} м/с \nПогодные условия: {desc} \n' \
               f'Восход: {sunrise} \nЗакат: {sunset}'
    except:
        return 'Ошибка получения данных'


root = ThemedTk(theme='arc')
root.title('World Weather')
root.geometry('500x400+550+250')
root.resizable(0, 0)

s = ttk.Style()
s.configure('TLabel', padding=20)
s.configure('.', font='Arial 11')

top_frame = ttk.Frame(root)
top_frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor='n')

entry = ttk.Entry(top_frame, font='Arial 11')
entry.place(relwidth=0.7, relheight=1)
entry.bind('<Return>', get_weather)

button = ttk.Button(top_frame, text='Запрос погоды', command=get_weather)
button.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = ttk.Frame(root)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor='n')

label = ttk.Label(lower_frame, anchor='nw')
label.place(relwidth=1, relheight=1)

root.mainloop()
