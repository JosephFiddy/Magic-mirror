from tkinter import *
from tkinter import font
import requests
import time
import cryptocompare
import random
from newsapi import NewsApiClient

"""
air quality in exeter api
"""


def get_weather():
    # retrieving all the data from weather API
    apikey = ""
    URL = "https://api.openweathermap.org/data/2.5/forecast"
    variables = {'APPID': apikey, 'q': 'Exeter, UK', 'units': 'metric'}
    response = requests.get(URL, params=variables)
    data = response.json()

    # extracting specific values
    temp = data['list'][0]['main']['temp']
    desc = data['list'][0]['weather'][0]['description']
    image = data['list'][0]['weather'][0]['icon']
    feels_like = data['list'][0]['main']['feels_like']

    return{'temparature': temp, 'description': desc, 'image': image, 'feels like': feels_like}


def clock():  # updating current_time label every second to show the current time
    format_time = time.strftime("%H:%M")
    format_seconds = time.strftime("%S")
    current_time['text'] = format_time
    seconds_clock['text'] = format_seconds
    root.after(1000, clock)


def date():  # updating date_label every second to show the current date
    format_date = time.strftime("%A, %B, %Y")
    date_label['text'] = format_date
    root.after(1000, date)


def get_btc_price():
    # retrieving the bitcoin price in gbp
    apikey = ""
    URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=GBP"
    response = requests.get(URL + '&api_key={' + apikey + '}')
    data = response.json()

    # updating the label
    bitcoin_tracker['text'] = "BTC: £" + str(int(data['GBP']))
    # update btc price in an hour - 3600000 milliseconds in an hour
    root.after(30000, get_btc_price)


def get_news():
    rand_category = random.choice(['science', 'business', 'health'])

    # have it search one of these random categories
    apikey = ""
    url = "https://newsapi.org/v2/top-headlines?"
    variables = {'country': 'gb', 'category': rand_category, 'apikey': apikey}
    response = requests.get(url, params=variables)
    data = response.json()

    rand_num = random.randint(0, len(data['articles'])+1)

    Title = data['articles'][random.randint(0, rand_num)]['title']
    desc = data['articles'][random.randint(0, rand_num)]['description']

    news_title['text'] = Title
    news_desc['text'] = desc
    root.after(300000, get_news)


root = Tk()
root.attributes('-fullscreen', True) # make main window full-screen
font = "Arial"

canvas = Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill=BOTH, expand=True) #configure canvas to occupy the whole main window

# clock graphics
clock_frame = Frame(root, bg="black")
clock_frame.place(relx=0.01, rely=0.01, relwidth=0.25, relheight=0.3)

clock_label = Label(clock_frame, bg="black")
clock_label.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)

date_label = Label(clock_frame, bg="black", anchor="w",
                   text="", font=(font, 24), fg="white")
date_label.place(relx=0.05, rely=0.1, relheight=0.15, relwidth=0.9)

current_time = Label(clock_frame, bg="black", anchor="w",
                     text="", font=(font, 58), fg="white")
current_time.place(relx=0.05, rely=0.27, relheight=0.4, relwidth=0.75)

seconds_clock = Label(clock_frame, bg="black", anchor="w",
                      text="", font=(font, 32), fg="white")
seconds_clock.place(relx=0.48, rely=0.22, relheight=0.4, relwidth=0.2)

# current weather graphics
weather_frame = Frame(root, bg="black")
weather_frame.place(relx=0.74, rely=0.01, relwidth=0.25, relheight=0.3)

weather = Label(weather_frame, bg="black")  #displays the border
weather.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)

Title = Label(weather_frame, bg="black", fg="white",
              font=(font, 24), text="Weather Forecast Exeter")
Title.place(relx=0.1, rely=0.1, relheight=0.2, relwidth=0.8)

# displaying current weather icon
icon = Canvas(weather_frame, bg="black", highlightbackground="black")
img = PhotoImage(file="C:\Python projects\Topics\Tkint er\img\\01d.png")

icon.create_image(70, 60, image=img)
icon.place(relx=0.1, rely=0.4, relheight=0.4, relwidth=0.3, anchor="nw")

Temperature = Label(weather_frame, bg="black", text=str(
    get_weather()['temparature']) + '°', font=(font, 34), fg="white")
Temperature.place(relx=0.45, rely=0.4, relheight=0.4, relwidth=0.45, anchor="nw")

feels_like = Label(weather_frame, bg="black", fg="white", text='feels like ' +
                   str(get_weather()['feels like']) + '°', font=(font, 14))
feels_like.place(relx=0.45, rely=0.8, relheight=0.15, relwidth=0.45, anchor="nw")

# bitcoin tracker in GBP
bitcoin_frame = Frame(root, bg="black")
bitcoin_frame.place(relx=0.01, rely=0.35, relwidth=0.15, relheight=0.15)

bitcoin_tracker = Label(bitcoin_frame, bg="black", text="", fg="white", font=(font, 22))
bitcoin_tracker.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)

# Display News headlines
news_frame = Frame(root, bg="black")
news_frame.place(relx=0.5, rely=0.85, relwidth=0.7, relheight=0.15, anchor="center")

news_title = Label(news_frame, text="", bg="black", fg="white", font=(font, 22))
news_title.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.45)

news_desc = Label(news_frame, text="", bg="black", fg="white", font=(font, 14))
news_desc.place(relx=0.01, rely=0.4, relwidth=0.98, relheight=0.45)

get_news()
get_btc_price()
clock()
date()
root.mainloop()

