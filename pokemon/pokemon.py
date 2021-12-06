import requests
import random
from os import system
from time import sleep
from math import ceil
import sys


class Pokemon:
    _weakness = {'fire': ['water'], 'grass': ['fire'], 'water': ['grass']}
    
    def __init__(self, name, element, hp):
        self.name = name
        self._HP = float(hp)
        self.hp = float(hp)
        self.element = element
        # self.attack = attack
        self.attacks = []
    
    def health(self):
        return self.hp
    
    def HPts(self):
        return self._HP
    
    def learn(self, attack):
        self.attacks.append(attack)
        
    def charge(self,  other, attack):
        boost = 1.5 if other._is_weak(attack) else 1      
        other.hp -= attack.damage * boost
        if other.hp < 0:
            other.hp = 0.0
            
    def is_alive(self):
        return self.health() > 0
    
    def _is_weak(self, attack):
        return attack.element in Pokemon._weakness[self.element]
    
    def recover(self, heal=None):
        if heal:
            self.hp += heal
            
        if self.health() > self._HP or not heal:
            self.hp = self._HP
        return self
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.element}, {self.health()}, {self.attacks})'


class Attack:
    def __init__(self, name, element, damage):
        self.name = name
        self.element = element
        self.damage = damage
        # self.power

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.element}, {self.damage})'

   
class Pokemons:
    def __init__(self, limit=10):
        self.pokemons = []
        self.limit = limit
        self.URL = 'https://pokeapi.co/api/v2'

    def load(self):
        res = requests.get(f'{self.URL}/pokemon/?limit={self.limit}')

        if res.ok:
            res = res.json()
            return res['results']
        return []


class Screen:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        
    def _space_constrains(self, name_length=12):
        div = 4
        base_space = int(self.screen_size - (name_length * 2))
        bar_length = int((base_space * (div - 1) / div) / 2)
        in_between_length = int(base_space * 1 / div)
        
        if bar_length % 2 == 0: 
            bar_length += 1
        
        if in_between_length % 2 != 0:
            in_between_length += 1 
        
        return name_length, bar_length, in_between_length
         
    def health_bar(self, pokemon, bar_length, fill='='):
        health_length = len(str(pokemon.HPts()))
        max_fill = int((bar_length - health_length - 3) / 2) # -3 chars from '[/]'
        steep = int(pokemon.HPts() / (bar_length - (health_length * 2)))
        fill_with = ceil(pokemon.health() / steep) # remove exrea fill right side
        
        if fill_with >= max_fill:
            right_fill = fill * (fill_with - max_fill)
            fill_with = max_fill
            health = f'{pokemon.health():=>{health_length}}'
        else:
            right_fill = ''
            health = f'{pokemon.health():>{health_length}}'
        
        
        left_fill = fill * fill_with 
        left = f'{left_fill:{max_fill}}{health}'
        right = f'{pokemon.HPts()}{right_fill:{max_fill}}'
 
        return f'[{left}/{right}]'
 
    def header(self, poke1, poke2, fill='-'):
        vs = "'VS'"
        name_length, bar_length, in_between_length = self._space_constrains()
        poke1_repr = f'{poke1.name.capitalize():{name_length}} {self.health_bar(poke1, bar_length)}'
        poke2_repr = f'{poke2.name.capitalize():{name_length}} {self.health_bar(poke2, bar_length)}'
        head = f'{poke1_repr}{vs:^{in_between_length}}{poke2_repr}'
        total_length = len(head)
        
        system('clear')
        print(
f"""
{fill * total_length}
{head}
{fill * total_length}
""")
        
    def winner(self, pokemon, delay=0.35):
        message = f'{pokemon.name} wins!!!!'.upper()
        message_len = len(message)
        for chunk in (message[:i] for i, _ in enumerate(message)):
            print(f'{chunk:>{int(self.screen_size / 2) + int(message_len / 2)}}', end='\r', flush=True)
            sleep(delay)
        print()
        
    def round(self, pokemon, rigth=False):
        spaces = int(self.screen_size * 5 / 8) if rigth else 0
        for i, attack in enumerate(pokemon.attacks, start=1): 
            print(f'{" ":>{spaces}}[{i}.] {attack.name}')




if __name__ == '__main__':
    try:
        screen_size = int(sys.argv[1])
    except:
        screen_size = None  
    
    screen_size = screen_size or 100
    screen = Screen(screen_size)
    
    system('clear')

    waterdragon = Pokemon('Waterdragon', 'grass', 183)
    charmander = Pokemon('Charmander', 'fire', 180)

    flamethrower = Attack("Flamethrower", 'fire', 25)
    water_gun = Attack("Tackle", 'water', 20)
    razor_leaf = Attack("Razor leaf", 'grass', 20)

    waterdragon.learn(water_gun)
    charmander.learn(flamethrower)


    while True:
        pokemons = [waterdragon.recover(), charmander.recover()]
        random.shuffle(pokemons)
        print('[1] ?????')
        print('[2] ?????')
        user = int(input('Pokemon: '))
        user_pokemon = pokemons.pop(user - 1)
        IA_pokemon = pokemons.pop()

        time_attack = random.choice((True, False))
        user_right_side = not time_attack
        IA_right_side = time_attack

        while user_pokemon.is_alive() and IA_pokemon.is_alive():
            system('clear')
            
            if user_right_side:
                screen.header(IA_pokemon, user_pokemon)
            else:
                screen.header(user_pokemon, IA_pokemon)
                
            if time_attack:
                screen.round(user_pokemon, user_right_side)
                index = int(input('Choose: '))
                attack = user_pokemon.attacks[index - 1]
                print(f'{user_pokemon.name} attack with {attack.name}')
                damage = user_pokemon.charge(IA_pokemon, attack)
                print(f'{IA_pokemon.name} recive {damage} damage points')
            else:
                screen.round(IA_pokemon, IA_right_side)
                attack = random.choice(IA_pokemon.attacks)
                print(f'{IA_pokemon.name} attack with {attack.name}')
                damage = IA_pokemon.charge(user_pokemon, attack)
                print(f'{user_pokemon.name} recive {damage} damage points')
                sleep(0.5)

            time_attack = not time_attack
            sleep(1.3)

        system('clear')
        
        screen.header(user_pokemon, IA_pokemon)    
        winner = IA_pokemon if IA_pokemon.is_alive() else user_pokemon
        screen.winner(winner)
        
        repeat = input('Another Battle (y/n)? :')
        if repeat.lower() == 'n':
            break
 
# pokemons = Pokemons(elemnts, 150)
# pokemons.load()
# print(pokemons.pokemons)
# for pok in filter(lambda pokemon: pokemon.element == 'fire', pokemons.pokemons):
#     print(pok)


# response = requests.get(f'{self.URL}/pokemon/{result["name"]}')
# if response.ok:
#     response = response.json()
#     element = response['types'][0]['type']['name']
#     if element in self.elements:
#         hp = response['stats'][0]['base_stat']
#         self.pokemons.append(Pokemon(result['name'], hp, element))