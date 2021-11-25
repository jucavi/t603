from IO import get_data, write_data
from distOps import distance_to
from screen import main_screen, by_date_screen, user_input, trip_planner
import requests

data = get_data()
URL = 'https://www.metaweather.com/api/location'


def get_url(url):
    try:
        return requests.get(url).json()
    except Exception:
        return [] 


def store_woeids(locations):
    initial_len = len(data.keys())
   
    for loc in locations:
        data[loc['title']] = loc['woeid']
    
    if initial_len < len(data.keys()):
        write_data(data)


def get_locations(city, loc=False):
    query = 'lattlong' if loc else 'query'
    
    return get_url(f'{URL}/search/?{query}={city}') 

     
def get_forecast(woeid, date=None, strict=True):  
    url = f'{URL}/{woeid}'
    if date:
        forecast = get_url(f'{url}/{date}/')
    else:
        forecast = get_url(url)
        if strict:
            forecast = forecast['consolidated_weather']
    return forecast

     
def show_forecast(city, forecast, limit=3):
    if forecast:
        print(f'\n{city} Forecast\n')
    for day in forecast[:limit]:
        print(f'For date:            {day["applicable_date"]}')
        print('---------------------')
        print(f'Maximun Temperature: {day["max_temp"]:3.3} ºC')
        print(f'Minimun Temperature: {day["min_temp"]:3.3} ºC')
        print(f'Temperature:         {day["the_temp"]:3.3} ºC')
        print(f'Humidity:            {day["humidity"]} %Hr')
        print(f'Wind:                {day["wind_direction_compass"]} {day["wind_speed"]:3.3} mph')
        print(f'Predictability:      {day["predictability"]} %')
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


def parse_latt_long(city):
    latt, long = city['latt_long'].split(',')
    
    return float(latt), float(long)


def from_to_distance(source, destination):           
    source = parse_latt_long(source)
    destination = parse_latt_long(destination)
    return distance_to(source, destination)


while True:
    main_screen()
    user = user_input()
    locations = []
    
    if user == 'Q':
        break

    if user == '1':
        query = user_input('City ')
        woeid = data.get(query)
        if not woeid:
            locations = get_locations(query)
            if locations:
                query, woeid = locations[0]['title'], locations[0]['woeid']
            else:
                print('No data Found.')
                continue
                  
        show_forecast(query, get_forecast(woeid))
            
    elif user == '2':
        query = user_input('Lattitude and longitude ')
        locations = get_locations(query, True)
        if locations:
            city, woeid = locations[0]['title'], locations[0]['woeid']
            show_forecast(city, get_forecast(woeid))
        else:
            print('No data Found.')
            
    elif user == '3':
        by_date_screen()
        try:
            query, loc, date = user_request()
            woeid = None
            if not loc:
                woeid = woeid = data.get(query)
            if not woeid:
                locations = get_locations(query, loc)
                query, woeid = locations[0]['title'], locations[0]['woeid']
            show_forecast(query, get_forecast(woeid, date))
        except:
            print('No data Found.')
            
    elif user == '4':
        try:
            source, destination, date = trip_planner()
            
            from_loc = get_locations(source)[0]['latt_long']
            dest_loc = get_locations(destination)[0]
            
            woeid_loc = data.get(destination)
            if not woeid_loc:
                destination, woeid_loc = dest_loc[0]['title'], dest_loc[0]['woeid']
            
            locations = get_locations(from_loc, True)
            from_city = locations.pop(0)
            dest_city = {}
            for candidate in locations:
                if candidate['title'] == destination:
                    dest_city = candidate
                    break
                
            if dest_city:
                distance =  (dest_city['distance'] - from_city['distance']) / 1000
            else:
                distance = from_to_distance(from_city, dest_loc)
                
            forecast = get_forecast(woeid_loc, date=date)[0]
            show_forecast(destination, forecast)
            
            if forecast[0]['weather_state_abbr'] in ('sn', 'sl', 'h', 't', 'hr'):
                print(f'Warning Weather state: *** {forecast[0]["weather_state_name"].upper()} ***')
            else:
                print(f'Weather state:       {forecast[0]["weather_state_name"]}')
                
            speed_limit = 10
            if forecast[0]['wind_speed'] > speed_limit:
                duration = distance / speed_limit
            else:
                duration = distance / 100
                
            print(f'Distance:            {round(distance)} Kilometers')
            print(f'Trip duration:       {round(duration)} h')  
        except Exception as e:
            # print(f'Exception raised: {e}')
            print('Sorry no data found or invalid input, try again.')
                   
    store_woeids(locations)