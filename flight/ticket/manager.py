from helpers import load_json_data, write_json_data
from datetime import timedelta
from models import Airport

airports_data = load_json_data('airports.json')

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
    return load_json_data('tickets.json')

def remove_ticket(identifier):
    tickets_data = load_json_data('tickets.json')
    tickets_data.pop(identifier)
    print('Deleted!')
    write_json_data(tickets_data, 'tickets.json', overwrite=True)

def update_ticket(identifier):
    origin_loc = identifier[:3]
    airports = airports_list()
    return airports[origin_loc]


if __name__ == '__main__':
    for airport in airports_list():
        print(airport)
