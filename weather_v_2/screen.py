def main_screen():
    print('\n########### Weather ###########\n')
    print('[1] By City')
    print('[2] By lattitude and longitude')
    print('[3] By City/Coord on date')
    print('[4] Get a trip')
    print('[Q] Exit')

   
def by_date_screen():
    print('\n####### Weather on Date #######\n')
    print('[1] By City')
    print('[2] By lattitude and longitude')
    print('Input Format: [option] (city/lattlong) (date: yyyy/mm/dd)')
    
    
def user_input(message=''):    
    return input(f'\n{message}>> ').strip().capitalize()