import requests
import random
import os
import time
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
    
    def health_bar(self, pokemon, fill='='):
        size = int(self.screen_size / 4)
        steep = int(pokemon.HPts() / size)
        center = round(size / 2)
        hp_repr = f'{pokemon.health()}/{pokemon.HPts()}'
        size_health = len(hp_repr)
        char_amount = int(pokemon.health() / steep - size_health)
        half_side = center - int(size_health / 2)
        right = fill * int(char_amount - half_side) if char_amount - half_side > 0 else ' '
        left = fill * char_amount if char_amount <= half_side else fill * half_side
        # TODO function only to make calcs (half side size health)
        
        # TODO other function
        return f'[{left.ljust(half_side)}{hp_repr.center(size_health)}{right.ljust(half_side)}]'

    
    def header(self, poke1, poke2, fill='-'):
        os.system('clear')
        half = int(self.screen_size / 2)
        poke1_repr = f'{poke1.name.capitalize()} {self.health_bar(poke1)}'
        poke2_repr = f'{poke2.name.capitalize()} {self.health_bar(poke2)}'
        vs = "'VS'"
        vs_length = int((self.screen_size - len(poke1_repr) - len(poke2_repr)) / 2)
        poke_length = int(half - (vs_length / 2))
        print(
f"""
{fill * self.screen_size}
{poke1_repr:{poke_length}}{vs:^{vs_length}}{poke2_repr:>{poke_length}}
{fill * self.screen_size}
""")
        
    def winner(self, pokemon, delay=0.35):
        message = f'{pokemon.name} wins!!!!'.upper()
        message_len = len(message)
        for chunk in (message[:i] for i, _ in enumerate(message)):
            print(f'{chunk:>{int(self.screen_size / 2) + int(message_len / 2)}}', end='\r', flush=True)
            time.sleep(delay)
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
    
    screen_size = screen_size or 126
    screen = Screen(screen_size)
    
    os.system('clear')

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
            os.system('clear')
            
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
                time.sleep(0.5)

            time_attack = not time_attack
            time.sleep(1.3)

        os.system('clear')
        
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