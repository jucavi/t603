def main_screen():
    print('\n########### Weather ###########\n')
    print('[1] By City')
    print('[2] By lattitude and longitude')
    print('[3] By City/Coord on date')
    print('[4] Itinerary planner')
    print('[Q] Exit')

   
def by_date_screen():
    print('\n####### Weather on Date #######\n')
    print('[1] By City')
    print('[2] By lattitude and longitude')
    print('Input Format: [option] (city/lattlong) (date: yyyy/mm/dd)')
    
def trip_planner():
    source = user_input('From ', sep='')
    destination = user_input('Destination ', sep='')
    date = user_input('Date yyyy/mm/dd')
    return source, destination, date
    
def user_input(message='', sep='\n'):    
    return input(f'{sep}{message}: ').strip().capitalize()