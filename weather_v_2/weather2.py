from IO import get_data, write_data
from distOps import distance_to
from screen import main_screen, by_date_screen, user_input
import requests

data = get_data()
URL = 'https://www.metaweather.com/api/location'


def get_url(url):
    try:
        return requests.get(url).json()
    except Exception:
        return [] 


def store_woeids(locs):
    initial_len = len(data.keys())
   
    for loc in locs:
        data[loc['title']] = loc['woeid']
    
    if initial_len < len(data.keys()):
        write_data(data)

def get_locations(city, loc=False):
    query = 'lattlong' if loc else 'query'
    
    return get_url(f'{URL}/search/?{query}={city}') 

     
def get_forecast(woeid, date=None):  
    url = f'{URL}/{woeid}'
    if date:
        forecast = get_url(f'{url}/{date}/')
    else:
        forecast = get_url(url)['consolidated_weather']        
            
    return forecast

     
def show_forecast(city, forecast, limit=3):
    print(f'\n{city} Forecast\n')
    for day in forecast[:limit]:
        print(f'For date:            {day["applicable_date"]}')
        print('---------------------')
        print(f'Maximun Temperature: {day["max_temp"]:3.3} ºC')
        print(f'Minimun Temperature: {day["min_temp"]:3.3} ºC')
        print(f'Temperature:         {day["the_temp"]:3.3} ºC')
        print(f'Humidity:            {day["humidity"]} %Hr')
        print(f'Wind:                {day["wind_direction_compass"]} {day["wind_speed"]:3.3} mph')
        input()

def user_request():
    user = user_input()
    loc = False
    try:
        option, value, date = user.split(' ')
    except Exception:
        print('Invalid input')
    
    if option == '2':
        loc = True
        
    return value, loc, date


if __name__ == '__main__':
    while True:
        main_screen()
        user = user_input() 

        if user == 'Q':
            break

        if user == '1':
            query = user_input('City ')
            locs = get_locations(query)
            if locs:
                show_forecast(locs[0]['title'], get_forecast(locs[0]['woeid']))
        elif user == '2':
            query = user_input('Lattitude and longitude ')
            locs = get_locations(query, True)
            if locs:
                show_forecast(locs[0]['title'], get_forecast(locs[0]['woeid']))
        elif user == '3':
            by_date_screen()
            try:
                query, loc, date = user_request()
            except:
                continue
            locs = get_locations(query, loc)
            show_forecast(locs[0]['title'], get_forecast(locs[0]['woeid'], date))
        elif user == '4':
            query = user_input('From ').capitalize()
            latt_long = get_data(city=query, trip=True)
            destinations = get_data(latt_long=latt_long)
            destination = user_input('To ').capitalize()
            for destination in  destinations:
                print(destination)
            
        store_woeids(locs)