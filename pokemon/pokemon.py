import requests
import random
import os
import time


class Pokemon:
    elements = ['fire', 'grass', 'water']
    
    def __init__(self, name, element, hp):
        self.name = name
        self.HP = hp
        self.hp = hp
        self.element = element
        self.attacks = []
        
        
    def learn(self, attack):
        self.attacks.append(attack)
        
    def attack(self,  other, attack):
        # Check elements ?
        if ((Pokemon.elements.index(other.element) == 0 and Pokemon.elements.index(attack.element) == 2)
            or (self.elements.index(attack.element) - self.elements.index(other.element) == 1)):
            damage = attack.damage * 1.5
        else:
            damage = attack.damage
            
        other.hp -= damage
        return damage
            
    def is_alive(self):
        return self.hp >= 0
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.element}, {self.hp}, {self.attacks})'


class Attack:
    def __init__(self, name, element, damage):
        self.name = name
        self.element = element
        self.damage = damage

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.element}, {self.damage})'

   
class Pokemons:
    def __init__(self, elements, limit=10):
        self.pokemons = []
        self.limit = limit
        self.elements = elements
        self.URL = 'https://pokeapi.co/api/v2'

        
    def load(self):
        res = requests.get(f'{self.URL}/pokemon/?limit={self.limit}')

        if res.ok:
            res = res.json()
            for result in res['results']:
                response = requests.get(f'{self.URL}/pokemon/{result["name"]}')
                if response.ok:
                    response = response.json()
                    element = response['types'][0]['type']['name']
                    if element in self.elements:
                        hp = response['stats'][0]['base_stat']
                        self.pokemons.append(Pokemon(result['name'], hp, element))
        
        
def hp_bar(pokemon):
    full = 25
    steep = int(pokemon.HP / full)
    level = '=' * int((pokemon.hp / steep))
    return f'[{level.ljust(full)}]'
    
    
os.system('clear')

waterdragon = Pokemon('Waterdragon', 'grass', 183)
charmander = Pokemon('Charmander', 'fire', 180)

flamethrower = Attack("Flamethrower", 'fire', 25)
water_gun = Attack("Tackle", 'water', 20)
razor_leaf = Attack("Razor leaf", 'grass', 20)

waterdragon.learn(water_gun)
charmander.learn(flamethrower)

while True:
    pokemons = [waterdragon, charmander]
    random.shuffle(pokemons)
    print('[1] ?????')
    print('[2] ?????')
    user = int(input('Pokemon: '))
    user_pokemon = pokemons.pop(user - 1)
    IA_pokemon = pokemons.pop()

    time_attack = random.choice((True, False))

    while user_pokemon.is_alive() and IA_pokemon.is_alive():
        os.system('clear')
        print(f'User: {user_pokemon.name} HP: {hp_bar(user_pokemon)}     IA: {IA_pokemon.name} HP: {hp_bar(IA_pokemon)}')
        if time_attack:
            for i, attack in enumerate(user_pokemon.attacks, start=1):
                print(f'[{1}.] {attack.name}')
            index = int(input('Choose: '))
            attack = user_pokemon.attacks[index - 1]
            print(f'{user_pokemon.name} attack with {attack.name}')
            damage = user_pokemon.attack(IA_pokemon, attack)
            print(f'{IA_pokemon.name} recive {damage} damage points')
        else:
            attack = random.choice(IA_pokemon.attacks)
            print(f'{IA_pokemon.name} attack with {attack.name}')
            damage = IA_pokemon.attack(user_pokemon, attack)
            print(f'{user_pokemon.name} recive {damage} damage points')
            time.sleep(0.5)

        time_attack = not time_attack
        time.sleep(1.3)

                
    winner = IA_pokemon if IA_pokemon.is_alive() else user_pokemon
    print(f'{winner.name} win!')
    
    repeat = input('Another Battle (y/n)? :')
    if repeat.lower() == 'n':
        break

# pokemons = Pokemons(elemnts, 150)
# pokemons.load()
# print(pokemons.pokemons)
# for pok in filter(lambda pokemon: pokemon.element == 'fire', pokemons.pokemons):
#     print(pok)