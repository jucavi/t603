import pickle

filename = 'cities_woeids.pck'

def woeid(city):
    try:
        with open(filename, 'rb') as file:
            cities_woeids = pickle.load(file)
    except Exception:
        return None
    else:
        return cities_woeids.get(city.lower(), None)
    
def database_append_woeid(city, woeid):
    cities_woeids = get_city_woeid_dict()
    cities_woeids[city.lower()] = woeid
    
    try:    
        with open(filename, 'wb') as file:
            pickle.dump(cities_woeids, file)
    except Exception as e:
        print(f'Unable open "{filename}" file')
        print(f'Error: {e.message}')
            
def get_city_woeid_dict():
    try:
        with open(filename, 'rb') as file:
            cities_woeids = pickle.load(file)            
    except Exception:
            cities_woeids = {}
    finally:
        return cities_woeids