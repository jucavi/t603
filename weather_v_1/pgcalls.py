import requests

URL = 'https://www.metaweather.com/api/location'

def city_by_name(city):
    query = f'{URL}/search/?query={city}'
    try:
        return requests.get(query).json()
    except Exception:
        return []

def city_by_lattlong(latt_long):
    query = f'{URL}/search/?lattlong={latt_long}'
    try:
        return requests.get(query).json()
    except Exception:
        return []
    
def data_weather(woeid):
    query = f'{URL}/{woeid}/'
    try:
        return requests.get(query).json()
    except Exception:
        return {}

def forecast_for_date(woeid, date):
    try:
        query = f'{URL}/{woeid}/{date}/'    
        return requests.get(query).json()
    except Exception:
        return []        


