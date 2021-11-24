import pgcalls as pg
import rwoeid as rw

cities_woeids = rw.get_city_woeid_dict()

def user_input(message=''):    
    return input(f'\n{message}>> ').strip().capitalize()

def display_forecast(forecast):
    for day_forecast in forecast:
        print(f'For date:            {day_forecast["applicable_date"]}')
        print(f'Maximun Temperature: {day_forecast["max_temp"]:3.3} ºC')
        print(f'Minimun Temperature: {day_forecast["min_temp"]:3.3} ºC')
        print(f'Temperature:         {day_forecast["the_temp"]:3.3} ºC')
        print(f'Humidity:            {day_forecast["humidity"]} %Hr')
        print(f'Wind:                {day_forecast["wind_direction_compass"]} {day_forecast["wind_speed"]:3.3} mph')
        user_input()      
          
def select_city(cities):
    user = user_input('\nSelect city ')
    try:
        return cities[int(user) - 1]["title"]
    except Exception:
        print('Selection error, retry (y/n)? ')
        ret = user_input()
        if ret.lower().startswith('y'):
            select_city(cities)
        return None 
        
        
def forecast_handler(cities):
    if len(cities) == 1:
        woeid = rw.woeid(cities[0]['title'])
        if not woeid:
            woeid = cities[0]['woeid']
            rw.database_append_woeid(cities[0]['title'], woeid)
            
        data = pg.data_weather(woeid)
        forecast = pg.forecast(data)
        
        print(f'\n{data["title"]} {data["timezone"]}\n')
        display_forecast(forecast[:3])
    else:
        cities_screen(cities)
        city = select_city(cities)
        if city:
            by_city(city)
        else:
            main_screen()

def get_woeid(city):
    if city in cities_woeids:  
        return cities_woeids[city]

    cities = pg.city_by_name(city)
    if len(cities) == 1:
        return cities[0]['woeid']
    
    return ''

def by_city(name = None):
    if not name:
        name = user_input('Weather on city ')
        
    if name in cities_woeids:  
        cities = pg.city_by_name([], cities_woeids[name])
    else:
        cities = pg.city_by_name(name)
    if cities:
        forecast_handler(cities)
    else:
        print(f'Error: No city found with that name {name}')
        
def by_latt_long():
    latt_long = user_input('Weather on lattitud and longitude separated by comma ')
    cities = pg.city_by_lattlong(latt_long)
    forecast_handler(cities)

def by_cc_date():
    data_request = user_input('Weather on city at date, in form >> <city> <year> <month> <day>')
    city, *rest = data_request.split(' ')
    date = '/'.join(rest[:3])
    woeid = get_woeid(city)
    display_forecast(pg.forecast_for_date(woeid, date))

def main_screen():
    print('\n########### Weather ###########\n')
    print('[1] By City')
    print('[2] By lattitude and longitude')
    print('[3] By City/Coord on date')
    print('[Q] Exit')
    
def cities_screen(cities):
    print(f'Found {len(cities)} cities, choose one:\n')
    for i, city in enumerate(cities, start=1):
        rw.database_append_woeid(city['title'], city['woeid'])
        print(f'[{i}] {city["title"]} woeid: {city["woeid"]}')

if __name__ == '__main__':
    while True:
        main_screen()
        user = user_input() 

        if user == 'Q':
            break
        
        if user == '1':
            by_city()
        elif user == '2':
            by_latt_long()
        elif user == '3':
            by_cc_date()
        
        
    