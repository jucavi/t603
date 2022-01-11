import requests
import time
import os
import threading

cwd = f'{os.path.dirname(__file__)}/flags'
url = 'https://restcountries.com/v3.1/all'


def get_urls_flags(url):
    res = requests.get(url).json()
    return (country['flags']['svg']for country in res)
    # return (country['flags']['png']for country in res)


def dowload_flag(url):
    res = requests.get(url)
    if res.ok:
        with open(f'{cwd}/{url[-6:]}', 'wb') as file:
            file.write(res.content)


print('--------------------------------------------')
print('|              Proccess start               |')
print('--------------------------------------------')
start = time.perf_counter()

urls_flags = get_urls_flags(url)

# for url in urls_flags:
#     dowload_flag(url)

for url in urls_flags:
    threading.Thread(target=dowload_flag, args=[url]).start()

finish = time.perf_counter()
print('--------------------------------------------')
print(f'|     End proccess in: {finish - start:.9f} secs     |')
print('--------------------------------------------')
