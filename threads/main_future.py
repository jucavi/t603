import requests
import time
import os
import threading
import concurrent.futures

cwd = f'{os.path.dirname(__file__)}/flags'
url = 'https://restcountries.com/v3.1/all'

if not os.path.exists(cwd):
    os.mkdir(cwd)

local_thread = threading.local()


def get_session():
    if not hasattr(local_thread, 'session'):
        local_thread.session = requests.Session()
    return local_thread.session


def get_urls_flags(url):
    res = requests.get(url).json()
    return [country['flags']['svg']for country in res]


def dowload_flag(url):
    session = get_session()
    with session.get(url) as response:
        with open(f'{cwd}/{url[-6:]}', 'wb') as file:
            file.write(response.content)


print('--------------------------------------------')
print('|              Proccess start               |')
print('--------------------------------------------')
start = time.perf_counter()

urls_flags = get_urls_flags(url)

# Sync
# for url in urls_flags:
#     dowload_flag(url)

# for url in urls_flags:
#     threading.Thread(target=dowload_flag, args=[url]).start()

with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls_flags)) as executor:
    executor.map(dowload_flag, urls_flags)

finish = time.perf_counter()
print('--------------------------------------------')
print(f'|     End proccess in: {finish - start:.9f} secs     |')
print('--------------------------------------------')
