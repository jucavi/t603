import requests
import os
import random

url = 'https://restcountries.com/v3.1/'

def get_region(name):
    region = requests.get(f'{url}/region/{name}')
    if region.ok:
        return  region.json()
    
    print('Not region found!')
    return []

   
def get_country(name, full=False):
    country = requests.get(f'{url}/name/{name}')
    if country.ok:
        country = country.json()[0]
        if full:
            return country
        else:
            return {
                'name': country['name']['common'],
                'capital': country['capital'][0],
                'region': country['region'],
                'population': country['population'],
                'area': country['area'],
                'flag': country['flags']['svg']
            }
    else:
        print(f'Error: {country.status_code}!\nCountry {name} not found!')
        return {}
    
    
def get_path(folder='flags'):
    dirname = os.path.join(os.path.dirname(__file__), folder)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        print(f'Created {folder} folder in current directory.')
    
    if dirname == folder:
        print(f'Unable to create "{folder}" folder\nReturn current directory!')
        return os.getcwd()
    
    return dirname
           
            
def export_flag_image(country, path=None):
    if not path:
        path = get_path()
        
    try:
        # Using flag <--
        """country = get_country(country, full=True)
        filename =  filename = f'{country["name"]["common"].lower()}.svg'"""

        filename = f'{country.get("name").lower()}.svg'
        filepath = os.path.join(path, filename)
        # If flag not saved yet
        if not os.path.exists(filepath):
            # Using flag <--
            """with open(filepath, 'wb') as file:
                    file.write(country['flag'].encode())
            print(f'Flag saved in {filepath}')"""
            
            res = requests.get(country.get('flag'))
            if res.ok:
                with open(filepath, 'wb') as file:
                    file.write(res.content)
                print(f'Flag saved in {filepath}')
        else:
            print(f'Flag already saved in {filepath}')
    except Exception:
        print('Missing country flag!')
        
        
def print_country(country):
    print()
    for key, value in country.items():
        if type(value) == list:
            print(f'{key.capitalize()}:')
            for item in value:
                print(f'  * {item}')
        else:
            print(f'{key.capitalize():<13}: {value}')


def main_screen():
    print('\n########## Nice App ##########\n')
    print(f'[1] Search Country')
    print(f'[2] Flag download')
    print(f'[3] Get Fun!')
    print(f'[Q] Quit')

    
def question_subjects(countries, size=None):
    if size:
        subjects = random.sample(countries,  size)
        answer = subjects[0]
        random.shuffle(subjects)
        return subjects, answer
    else:
        return random.choice(countries)


def get_value(subject, search_path):
    try:
        for key in search_path:
            if isinstance(subject, dict):
                subject = subject.get(key)
            elif isinstance(subject, list):
                subject = subject[key]
        return subject
    except Exception:
        print('Check your keys in seach path paramenter')


def option_menu(subjects, answer, search_path):
    print(f'{search_path[0].capitalize()} of {answer["name"]["common"]}:')
    for i, subject in enumerate(subjects, 1):
        print(f'  [{i}] {get_value(subject, search_path)}')

      
def print_answer_success(is_ok):
    if is_ok:
        print(random.choice(['Weell done!', 'Amazing!', 'Great job!']))
    else:
        print(random.choice(['Keep trying!', 'Nice try!']))
    print()


def option_questions_generator(countries, search_paths, track, size=3,):
    search_path = random.choice(search_paths)
    subjects, answer = question_subjects(countries, size)
    search = (search_path, answer)
    
    if search in track:
        return None
    
    track.append(search)
        
    option_menu(subjects, answer, search_path)  
    try:
        user = int(input(': '))
        if user <= 0:
            raise IndexError
        
        subject = subjects[user - 1]
    except Exception:
        print('Invalid input')
        return False
    return subject == answer


def max_min_question_generator(region, search_paths, track):
    search_path = random.choice(search_paths)
    func, verb = (max, 'biggest') if random.choice((True, False)) else (min, 'smallest')
    search = (search_path, func)

    if search in track:
        return None
    
    track.append(search)
    subject = input(f'Country with {verb} {search_path[0]}: ').lower()

    return subject == func(region, key=lambda x: get_value(x, search_path))['name']['common'].lower() 


while True:
    main_screen()
    user = input(': ')
    
    if user.lower() == 'q':
        break
    
    if user == '1':
        """
        1. Get Country
        2. Search Country
        3. Print
        """
        country = input('\nCountry to searh: ')
        print_country(get_country(country))
        input()
    
    elif user == '2':
        """
        1. Get country
        """
        country = input('\nCountry\'s flag: ')
        # Using flag 
        # export_flag_image(country)
        export_flag_image(get_country(country))
        input()

    elif user == '3':
        """
        Game
        1. Get a continent
        2. Questions whith score counter
            - Three posible answers questions
            - Max, min questions
        3. choose correct answer
        """
        option_paths = (('capital', 0), ('population',), ('area',))
        max_min_paths = (('population',), ('area',))
        num_of_questions = 10    
        questions = (
            (option_questions_generator, option_paths), 
            (max_min_question_generator, max_min_paths)
        )
        track = []
        iterations = 0
        success = 0
        
        region_search = input('\nRegion to play with: ')
        print()
        region = get_region(region_search)

        if region:
            while iterations < num_of_questions:
                question, search_paths = random.choice(questions)
                is_ok = question(region, search_paths, track)
                if is_ok == None:
                    continue
                elif is_ok:
                    success +=1
                    
                print_answer_success(is_ok)
                iterations += 1
            
            print(f'{success} correct answers, {success / num_of_questions * 100:.1f}% assertions')


# region = get_region('europe')
# negative_area = list(filter(lambda x: x['area'] < 0, region))
# Svalbard and Jan Mayen

# ['Asia', 'Africa', 'Americas', 'Europe', 'Antarctic', 'Oceania']"
# url = 'https://restcountries.com/v3.1/all'
# all_countries = requests.get(url).json()
# print(set(map(lambda x: x['region']), all_countries))
# negative_area = list(filter(lambda x: x['area'] < 0, all_countries))
