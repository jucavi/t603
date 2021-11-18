import requests
import csv
import os
import sys
from functools import reduce
import matplotlib.pyplot as plt

path = os.path.dirname(__file__)
url = 'https://datos.comunidad.madrid/catalogo/dataset/032474a0-bf11-4465-bb92-392052962866/resource/ee750429-1e05-411a-b026-a57ea452a34a/download/municipio_comunidad_madrid.csv'


# Data download
def get_data_from_url(url):
    try:
        response = requests.get(url)
    except Exception:
        print(f'Unable to connect to: {url}')
    else:
        if response.ok:
            return response.content.decode('utf-8', errors='replace')
        else:
            print(f'Error: Status code {response.status_code}')
            return None

# Write to csv file
def write_raw_data_to(data, filename, path='.'):
    try:
        with open(os.path.join(path, filename), 'w') as file:
            file.write(data)
    except Exception as e:
        print('Error: {e.message}')
        
# Read data from csv file   
def read_dataframe(file_path, delimiter=';'):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=delimiter)
            data = list(csv_reader)
    except Exception as e:
        print(f'Unable to read from {file_path}')
        print('Error: {e.message}')
    else:
        return data

def search_by_ine(dataframe, ine_code):
    for row in dataframe:
        if row[2] == ine_code:
            return row
    return None

def get_bigest_area(dataframe):
    return max(row[-2] for row in dataframe)

def get_bigest_citys_area(dataframe):
    max_area = 0
    city = []
    for row in dataframe:
        if row[-2] > max_area:
            max_area = row[-2]
            city.append(row)           
    return city
            
def get_total_surface(dataframe, use_reduce=True):
    if use_reduce:
        return reduce(lambda x, y: x + y, (float(row[-2]) for row in dataframe))
    return sum(float(row[-2]) for row in dataframe)

def get_total_population_density(dataframe, use_reduce=True):
    if use_reduce:
        return reduce(lambda x, y: x + y, (float(row[-1]) for row in dataframe))
    return sum(float(row[-1]) for row in dataframe)

def get_population_of(dataframe, city):
    for row in dataframe:
        if row[1].strip() == city.capitalize():
            return float(row[-2]) * float(row[-1])

def get_population(dataframe):
    return [float(row[-2]) * float(row[-1]) for row in dataframe]

def get_population_median(dataframe, method=''):
    total_population = 0
    
    if method == 'reduce':
        total_population = reduce(lambda x, y: x + y, (float(row[-2]) * float(row[-1]) for row in dataframe))
    elif method == 'sum':
        total_population = sum(float(row[-2]) * float(row[-1]) for row in dataframe)
    else:
        for row in dataframe:
            total_population += float(row[-2]) * float(row[-1])
    
    return total_population / len(dataframe)

# Returns (first_digit, probability) [1 <= digit <=9]
def get_first_significant_digit_distribution(numerical_set):
    distribution = {}
    # Operates over list and generators
    len_data = numerical_set.__sizeof__()
    for num in numerical_set:
        if str(num)[0]:
            distribution[str(num)[0]] = distribution.get(str(num)[0], 0) + 1
    
    return [(key, value / len_data) for key, value in distribution.items()]

def parse_to_axis(distribution):
    x_axe = []
    y_axe = []
    for x, y in distribution:
        x_axe.append(x)
        y_axe.append(y)
    return x_axe, y_axe 
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'municipios_madrid.csv'
           
    file_path = os.path.join(path, filename)     

    if not os.path.isfile(file_path) or len(sys.argv) > 1:
        data = get_data_from_url(url)
        if data:
            write_raw_data_to(data, filename, path)

    df = read_dataframe(file_path)[1:]

    print('With reduce:', get_total_population_density(df))
    print('Without reduce:', get_total_population_density(df, use_reduce=False))
    print('Population:', get_population_of(df, 'madrid'))
    
    print('Median with reduce:', get_population_median(df, method='reduce'))
    print('Median with sum:', get_population_median(df, method='sum'))
    print('Median:', get_population_median(df))

    # Testing get_first_significant_digit_distribution with list and generator
    density = [float(row[-1]) for row in df]
    area = (float(row[-2]) for row in df)
    population = get_population(df)
    
    density_distribution = get_first_significant_digit_distribution((density))
    area_distribution = get_first_significant_digit_distribution((area))
    population_distribution = get_first_significant_digit_distribution((population))
    # print(population)
    
    density_distribution = sorted(density_distribution, key=lambda x: x[0])
    area_distribution = sorted(area_distribution, key=lambda x: x[0])
    population_distribution = sorted(population_distribution, key=lambda x: x[0])
    
    fig = plt.figure(figsize=(18, 5))
    fig.suptitle('Belford\'s Law')
    x, y = parse_to_axis(density_distribution)
    plt.subplot(131)
    plt.ylabel('Population Density')
    plt.bar(x, y)

    plt.subplot(132)
    x, y = parse_to_axis(area_distribution)
    plt.ylabel('Surface Area')
    plt.bar(x, y)
    
    plt.subplot(133)
    x, y = parse_to_axis(population_distribution)
    plt.ylabel('Population')
    plt.bar(x, y)
    plt.show()
