import requests
import rwoeid
import math

data = rwoeid.get_data()
# Earth radius
R = 6371e3
URL = 'https://www.metaweather.com/api/location'

def user_input(message=''):    
    return input(f'\n{message}>> ').strip().capitalize()

def phi(latt):
    return float(latt) * math.pi / 180

def delta(source_coord, target_coord):
    return (float(target_coord) - float(source_coord)) * math.pi / 180

def distance(source, target):
    try:
        source_latt, source_long = source.split(',')
        target_latt, target_long = target.split(',')
        
        source_phi = phi(source_latt)
        target_phi = phi(target_latt)
        delta_phi = delta(source_latt, target_latt)
        delta_lambda = delta(source_long, target_long) 
        
        a = math.sin(delta_phi/2) * math.sin(delta_phi/2) \
            + math.cos(source_phi) * math.cos(target_phi/2) \
            * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
            
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c     
    except Exception as e:
        print(e)
        return 0

def get_url(url):
    try:
        print(f'GET: {url}')
        return requests.get(url).json()
    except Exception:
        return [] 
    
def get_woeid(locs):
    initial_len = len(data.keys())
    for loc in locs:
        data[loc['title']] = loc['woeid']
    
    if initial_len < len(data.keys()):
        rwoeid.write_data(data)
    
    if locs:
        return locs[0]['woeid']
    return None
        
def get_data(**kwargs):
    if kwargs.get('city'): 
        value = kwargs['city'].capitalize().strip()
        search = 'query'
    elif kwargs.get('latt_long'):
        value = kwargs['latt_long'].strip()
        search = 'lattlong'
    
    woeid = data.get(kwargs.get('city'))
    
    if not woeid:
        print('Getting woeid from:')
        locs = get_url(f'{URL}/search/?{search}={value}')
        woeid = get_woeid(locs)
        
    
    if woeid:
        url = f'{URL}/{woeid}'
        if kwargs.get('trip'):
            return get_url(url)['latt_long']
        
        try:
            if kwargs.get('date'):
                date = kwargs['date'].strip()
                forecast = get_url(f'{url}/{date}/')
            else:
                forecast = get_url(url)['consolidated_weather']        
        except Exception:
            return []
            
        return forecast
          
def show_forecast(forecast):
    for day in forecast[:3]:
        print(f'For date:            {day["applicable_date"]}')
        print('---------------------')
        print(f'Maximun Temperature: {day["max_temp"]:3.3} ºC')
        print(f'Minimun Temperature: {day["min_temp"]:3.3} ºC')
        print(f'Temperature:         {day["the_temp"]:3.3} ºC')
        print(f'Humidity:            {day["humidity"]} %Hr')
        print(f'Wind:                {day["wind_direction_compass"]} {day["wind_speed"]:3.3} mph')
        print()
        input()
        
def main_screen():
    print('\n########### Weather ###########\n')
    print('[1] By City')
    print('[2] By lattitude and longitude')
    print('[3] By City/Coord on date')
    print('[4] Get a trip')
    print('[Q] Exit')
    
def by_date_screen():
    print('\n####### Weather on Date #######\n')
    print('[1] By City')
    print('[2] By lattitude and longitude')
    print('[option] (city/lattlong) (date: yyyy/mm/dd) input format')

def user_request():
    user = user_input()
    try:
        option, value, date = user.split(' ')
        if option == '1':
            key = 'city'
        elif option == '2':
            key = 'latt_long'
    except Exception:
        print('Invalid input')
        return
        
    return {key: value, 'date': date}

if __name__ == '__main__':
    # scenarios = {
    #     'city' : {'city': 'Madrid'}, 
    #     'lattitude, longitude': {'latt_long': '40.42,-3.70'},
    #     'date and city': {'latt_long': '40.42,-3.70', 'date': '2021/11/26'},
    #     'date and (lattitude, longitud)': {'city': 'Madrid', 'date': '2021/11/26'},
    # }
    
    # for key, value in scenarios.items():
    #     print(f'By {key}: ')
    #     forecast = get_forecast(**value)
    #     show_forecast(forecast)
    #     print('\n######################################\n')
        
    # for latt in range(90):
    #     for long in range(90):
    #         lattlong = f'{latt},{long}'
    #         forecast = get_forecast(latt_long=lattlong)
    
    while True:
        main_screen()
        user = user_input() 

        if user == 'Q':
            break
        
        if user == '1':
            query = user_input('City ')
            show_forecast(get_data(city=query))
        elif user == '2':
            query = user_input('Lattitude and longitude ')
            show_forecast(get_data(latt_long=query))
        elif user == '3':
            by_date_screen()
            query = user_request()
            show_forecast(get_data(**query))
        elif user == '4':
            query = user_input('From ').capitalize()
            latt_long = get_data(city=query, trip=True)
            destinations = get_data(latt_long=latt_long)
            destination = user_input('To ').capitalize()
            for destination in  destinations:
                print(destination)
            
