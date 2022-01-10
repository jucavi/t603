import os
import platform
import json
from datetime import datetime, timedelta
from functools import wraps

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def fullpath(filename, path=''):
    path = path or os.path.dirname(__file__)
    return os.path.join(path, filename)

def load_json_data(filename, path=''):
    try:
        with open(fullpath(filename, path)) as f:
            return json.load(f)
    except Exception:
        return {}

def write_json_data(data, filename, path='', overwrite=False):
    filepath = fullpath(filename, path)

    if os.path.exists(filepath):
        if not overwrite:
            print(f'{filename} already exists!')
            overwrite = input('Confirm overwriting (Y/n): ').lower() == 'y'

    if overwrite:
        with open(filepath, 'w+') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def update_json_data(data, filename, path=''):
    filepath = fullpath(filename, path)

    with open(filepath, 'a+') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def clear_await(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        clear()
        result = func(*args, **kwargs)
        input('\nPress Enter to continue...')
        return result
    return wrapper

def ticket(filename, path=''):
    def decorator(klass):
        @wraps(klass)
        def flight_wrapper(*args, **kwargs):
            flight = klass(*args, **kwargs)
            dtime = datetime.utcnow()
            tickets = load_json_data(filename, path)

            tracker, ticket = flight.dict_ticket()
            counter = flight_wrapper.counter.get(tracker, 0)
            flight_wrapper.counter[tracker] = counter + 1
            tracker = f'{tracker}{flight_wrapper.counter[tracker]:04d}'
            ticket.update({'timestamp': dtime.strftime('%H:%M UTC'), 'id': tracker})
            tickets.update({tracker: ticket})

            write_json_data(tickets, filename, overwrite=True)
            return flight, tracker
        flight_wrapper.counter = {}
        return flight_wrapper
    return decorator

def f2delta(hours):
    return timedelta(hours=float(hours))

def set_tomorrow(strtime):
    tomorrow = datetime.now().date() + timedelta(days=1)
    time = datetime.strptime(strtime, '%H:%M').time()
    return datetime.combine(tomorrow, time)
