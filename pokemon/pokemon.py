import requests
import random
from os import system
from time import sleep
from math import ceil
import sys


class Pokemon:
    def __init__(self, name, element, hp, attack, defense, moves=None, dmg_relation=None):
        self.level = 1
        self.name = name
        self.element = element
        self._HP = float(hp)
        self.hp = float(hp)
        self.attack = attack
        self.defense = defense
        self.moves = moves or []
        self._dmg_relation = dmg_relation or []

    def effectiveness(self, other):
        relation = filter(lambda relation: other.element in relation.values, self._dmg_relation)
        try:
            return list(next(relation).keys())[0]
        except:
            return 1

    def damage(self, other, attack):
        targets = 1
        weather = 1
        badge = 1
        critical = 1
        STAB = 1
        burn = 1
        rand = random.uniform(.65, 1)
        effectiveness = self.effectiveness(other)
        
        return (((((2 * self.level) / 5 + 2) * attack.power * self.attack / other.defense) / 50) + 2) * targets * weather * badge * critical * rand * STAB * effectiveness * burn

    def health(self):
        return self.hp

    def HPpts(self):
        return self._HP

    def learn(self, attack):
        self.moves.append(attack)

    def charge(self,  other, attack):
        other.hp -= self.damage(other, attack)
        other.hp = round(other.hp, 1)
        if other.hp < 0:
            other.hp = 0.0

    def is_alive(self):
        return self.health() > 0

    def recover(self, heal=None):
        if heal:
            self.hp += heal

        if self.health() > self._HP or not heal:
            self.hp = self._HP
        return self
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.element}, {self.health()}, {self.attack}, {self.defense}, {self.moves}, {self._dmg_relation})'


class Attack:
    def __init__(self, name, dammage_class, power):
        self.name = name
        self.dammage_class = dammage_class
        self.power = power

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.dammage_class}, {self.power})'


class PokeGenerator:
    def __init__(self, pokemon_limit=10, moves_limit=5):
        self._pokemon_limit = pokemon_limit
        self._moves_limit = moves_limit
        self._URL = 'https://pokeapi.co/api/v2'
        self.pokemons = self._poke_generator()

    def _load(self):
        res = requests.get(f'{self._URL}/pokemon/?limit={self._pokemon_limit}')

        if res.ok:
            res = res.json()
            return res['results']
        return []
    
    def _pokemon(self, result):
        res = requests.get(result['url'])
        
        if res.ok:
            res = res.json()
            name = res['name']
            element = res['types'][0]['type']['name'] # TODO mixed types!!! only gets one
            hp = res['stats'][0]['base_stat']
            attack = res['stats'][1]['base_stat']
            defense = res['stats'][2]['base_stat']
            raw_moves = res['moves'][:self._moves_limit] # Only moves_limit moves
            moves = self._parse_moves(raw_moves)
            dmg_effectiveness = self._parse_effectiveness(f'{self._URL}/type/{element}')
            return Pokemon(name, element, hp, attack, defense, moves, dmg_effectiveness)
    
    def _parse_effectiveness(self, url):
        efectiveness_list = []
        res =  requests.get(url)
        if res.ok:
            translator = {'double_damage_to': 2, 'half_damage_to': 0.5, 'no_damage_to': 0}
            res = res.json()
            for key, key_value in translator.items():
                elements_dict = res['damage_relations'].get(key, [])
                if elements_dict:
                    elements = [element['name'] for element in elements_dict]
                    efectiveness_list.append({key_value: elements})

        return efectiveness_list
    
    def _parse_moves(self, raw_moves):
        moves = []
        urls = (move['move']['url']for move in raw_moves)
        for url in urls:
            res = requests.get(url)
            if res.ok:
                res = res.json()
                if res['power']:
                    moves.append(Attack(res['name'], res['damage_class']['name'], res['power']))
        return moves
    
    def _poke_generator(self):
        results = self._load()
        return (self._pokemon(result) for result in results)        


class Screen:
    def __init__(self, screen_size=100, name_length=12):
        self.screen_size = screen_size
        self.name_length = name_length
        self.bar_length, self.in_between_length = self._space_constrains()

    def _space_constrains(self):
        div = 4
        base_space = int(self.screen_size - (self.name_length * 2))
        bar_length = int((base_space * (div - 1) / div) / 2)
        in_between_length = int(base_space * 1 / div)

        if bar_length % 2 == 0: 
            bar_length += 1

        if in_between_length % 2 != 0:
            in_between_length += 1 

        return bar_length, in_between_length

    def health_bar(self, pokemon, fill='='):
        health_length = len(str(pokemon.HPpts()))
        max_fill = int((self.bar_length - (health_length * 2) - 3)) # -3 chars from '[ / ]'
        side_fill = int(max_fill / 2)
        steep = pokemon.HPpts() / max_fill
        fill_with = ceil(pokemon.health() / steep)
        fill_with = max_fill if fill_with > max_fill else fill_with

        if fill_with >= side_fill:
            right_fill = fill * (fill_with - side_fill)
            fill_with = side_fill
            health = f'{pokemon.health():=>{health_length}}'
        else:
            right_fill = ''
            health = f'{pokemon.health():>{health_length}}'


        left_fill = fill * fill_with 
        left = f'{left_fill:{side_fill}}{health}'
        right = f'{pokemon.HPpts()}{right_fill:{side_fill}}'

        return f'[{left}/{right}]'

    def header(self, poke1, poke2, fill='-'):
        vs = "'VS'"
        poke1_repr = f'{poke1.name.capitalize():{self.name_length}} {self.health_bar(poke1)}'
        poke2_repr = f'{poke2.name.capitalize():{self.name_length}} {self.health_bar(poke2)}'
        head = f'{poke1_repr}{vs:^{self.in_between_length}}{poke2_repr}'
        self.screen_size = len(head)

        system('clear')
        print(
f"""
{fill * self.screen_size}
{head}
{fill * self.screen_size}
""")

    # TODO  
    # position center, right, left
    # message printed left to right, right to left

    def fancy_message(self, message, left_direction=True, delay=0.35):
        message_len = len(message)
        if left_direction:
            for chunk in (message[:i] for i, _ in enumerate(message)):
                print(f'{chunk:>{int(self.screen_size / 2) + int(message_len / 2)}}', end='\r', flush=True)
                sleep(delay)
        else:
            for letter in message:
                print(f'{letter:>{int(self.screen_size / 2) - int(message_len / 2)}}', end='', flush=True)
                sleep(delay)

    def moves_display(self, pokemon, home=False):
        spaces =  0 if home else int((self.screen_size / 2) + int(self.in_between_length) / 2)
        for i, attack in enumerate(pokemon.moves, start=1):
            print(f'{"":>{spaces}}[{i}.] {attack.name}')




if __name__ == '__main__':
    # try:
    #     screen_size = int(sys.argv[1])
    # except:
    #     screen_size = None

    # screen_size = screen_size or 100
    # screen = Screen(screen_size)

    # system('clear')

    # waterdragon = Pokemon('Waterdragon', 'grass', 183, 25, 20)
    # charmander = Pokemon('Charmander', 'fire', 180, 25, 20)

    # flamethrower = Attack("Flamethrower", 'fire', 25)
    # water_gun = Attack("Tackle", 'water', 20)
    # razor_leaf = Attack("Razor leaf", 'grass', 20)

    # waterdragon.learn(water_gun)
    # charmander.learn(flamethrower)


    # while True:
    #     pokemons = [waterdragon.recover(), charmander.recover()]
    #     random.shuffle(pokemons)
    #     print('[1] ?????')
    #     print('[2] ?????')
    #     user = int(input('Pokemon: '))
    #     user_pokemon = pokemons.pop(user - 1)
    #     IA_pokemon = pokemons.pop()

    #     time_attack = random.choice((True, False))
    #     user_right_side = not time_attack
    #     IA_right_side = time_attack

    #     while user_pokemon.is_alive() and IA_pokemon.is_alive():
    #         system('clear')
            
    #         if user_right_side:
    #             screen.header(IA_pokemon, user_pokemon)
    #         else:
    #             screen.header(user_pokemon, IA_pokemon)

    #         if time_attack:
    #             screen.orderly_turn(user_pokemon, user_right_side)
    #             index = int(input('Choose: '))
    #             attack = user_pokemon.moves[index - 1]
    #             print(f'{user_pokemon.name} attack with {attack.name}')
    #             damage = user_pokemon.charge(IA_pokemon, attack)
    #             print(f'{IA_pokemon.name} recive {damage} damage points')
    #         else:
    #             screen.orderly_turn(IA_pokemon, IA_right_side)
    #             attack = random.choice(IA_pokemon.moves)
    #             print(f'{IA_pokemon.name} attack with {attack.name}')
    #             damage = IA_pokemon.charge(user_pokemon, attack)
    #             print(f'{user_pokemon.name} recive {damage} damage points')
    #             sleep(0.5)

    #         time_attack = not time_attack
    #         sleep(1.3)

    #     system('clear')

    #     screen.header(user_pokemon, IA_pokemon)
    #     winner = IA_pokemon if IA_pokemon.is_alive() else user_pokemon
    #     message = f'{winner.name} wins!!!!'.upper()
    #     screen.fancy_message(message)

    #     repeat = input('Another Battle (y/n)? :')
    #     if repeat.lower() == 'n':
    #         break

    pokemons = PokeGenerator(pokemon_limit=3).pokemons

    for pokemon in pokemons:
        print(pokemon, '\n')
