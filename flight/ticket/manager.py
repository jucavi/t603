from helpers import load_json_data, write_json_data
from datetime import timedelta
from models import Airport

airports_data = load_json_data('airports.json')
tickets_data = load_json_data('tickets.json')

def airports_list():
    airports = dict()
    for loc, raw_data in airports_data.items():
        city = raw_data['city']
        name = raw_data['airport_name']
        utc = timedelta(hours=raw_data['UTC'])
        flights = raw_data['dest']
        airports[loc] = (Airport(loc, city, name, utc, flights))
    return airports

def ticket_list():
    return tickets_data

def remove_ticket(identifier):
    try:
        tickets_data.pop(identifier)
        print('deleting...')
        write_json_data(tickets_data, overwrite=True)
    except:
        return None


if __name__ == '__main__':
    for airport in airports_list():
        print(airport)
