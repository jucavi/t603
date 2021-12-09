import requests

url = 'https://restcountries.com/v3.1/all'

countries = requests.get(url).json()

by_cont = {}
for country in countries:
    if by_cont.get(country['region']):
        by_cont[country['region']].append(country)
    else:
        by_cont[country['region']] = [country]

        
print(by_cont.keys())
print(set(map(lambda x: x['region'], countries)))

by_region = [{region: list(filter(lambda x: x['region'] == region, countries))} for region in set(map(lambda x: x['region'], countries))]

print(len(by_region))
