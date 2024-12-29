#!/usr/bin/env python

import json
import requests
from datetime import datetime
from pathlib import Path
from geopy.geocoders import Nominatim
# import os


def extract_numbers(text):
    try:
        first, second = text.split(",")
        return first, second
    except ValueError:
        return 0, 0


# bonnjalal is my username
long_lati = "34.03313,-5.00028" # your location longitude and latitude
# if you left the @long_lati empty the script will try to get it from internet using your ip adress
if long_lati == "":
    ip = requests.get("http://ipinfo.io/json").json()
    long_lati = ip["loc"]
    # city = ip["city"]
    location_file.write_text(long_lati)

DAY = datetime.now().day
YEAR = datetime.now().year
MONTH = datetime.now().month
LATITUDE, LONGITUDE = extract_numbers(long_lati)

geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.reverse(LATITUDE + "," + LONGITUDE)
address = location.raw["address"]
city = address.get("city", "")
country = address.get("country", "")

athan = requests.get(
    f"http://api.aladhan.com/v1/calendar/{YEAR}/{MONTH}?latitude={LATITUDE}&longitude={LONGITUDE}&method=3"
).json()

text = "  🕋︎ "

tooltip = f"<b>المدينة: {city}, {country} </b>\n"
tooltip += f"<b>ميلادي: {athan['data'][DAY-1]['date']['gregorian']['date']}</b>\n"
tooltip += f"<b>هجري: {athan['data'][DAY-1]['date']['hijri']['date']}</b>\n"

tooltip += f"الفجر: {athan['data'][DAY-1]['timings']['Fajr']}\n"
tooltip += f"الشروق: {athan['data'][DAY-1]['timings']['Sunrise']}\n"
tooltip += f"الظهر: {athan['data'][DAY-1]['timings']['Dhuhr']}\n"
tooltip += f"العصر: {athan['data'][DAY-1]['timings']['Asr']}\n"
tooltip += f"المغرب: {athan['data'][DAY-1]['timings']['Maghrib']}\n"
tooltip += f"العشاء: {athan['data'][DAY-1]['timings']['Isha']}\n"

out_data = {
    "text": text,
    # "alt": status,
    "tooltip": tooltip,
    # "class": status_code,
}
print(json.dumps(out_data))
