from helpers import load_json_data
from datetime import timedelta
from models import Airport

data = load_json_data('airports.json')

def airports_list():
    airports = dict()
    for loc, raw_data in data.items():
        city = raw_data['city']
        name = raw_data['airport_name']
        utc = timedelta(hours=raw_data['UTC'])
        flights = raw_data['dest']
        airports[loc] = (Airport(loc, city, name, utc, flights))
    return airports


if __name__ == '__main__':
    for airport in airports_list():
        print(airport)
