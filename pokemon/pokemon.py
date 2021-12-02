import requests
import random

URL = 'https://pokeapi.co/'
elemnts = ['fire', 'water', 'grass']

class Pokemon:
    def __init__(self, name, element, hp, attacks=None):
        self.name = name
        self.element = element
        self.hp = hp
        self.attacks = attacks or []
        
    def learn(self, attack):
        self.attacks.append(attack)
        
    def attack(self,  other, attack):
        # Check elements ?
        other.hp -= attack.damage
    
    def __str__(self):
        return f'{self.__class__.__name__}({self.name}, {self.element}, {self.hp}, {self.attacks})'

class Attack:
    def __init__(self, name, element, damage):
        self.name = name
        self.element = element
        self.damage = damage

    def __str__(self):
        return f'{self.__class__.__name__}({self.name}, {self.element}, {self.damage})'
    

pikachu = Pokemon('Pikachu', 'electric', 180)
charmander = Pokemon('Charmander', 'fire', 183)

fire_attack = Attack('Flametrower', 'fire', 52)
electric_attack = Attack('Static', 'electric', 55)

pikachu.learn(electric_attack)
charmander.learn(fire_attack)


pokemons = [pikachu, charmander]
random.shuffle(pokemons)
print('[1] ?????')
print('[2] ?????')
user = int(input('Pokemon: '))
user_pokemon = pokemons.pop(user)
IA_pokemon = pokemons.pop()

time_attack = random.choice((True, False))

while user_pokemon.hp > 0 and IA_pokemon.hp > 0:
    if time_attack:
        user_pokemon.attack(IA_pokemon, user_pokemon.attacks[0])
    else:
        IA_pokemon.attack(user_pokemon, IA_pokemon.attacks[0])
        
    time_attack = not time_attack
    
print(user_pokemon)
print(IA_pokemon)