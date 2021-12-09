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
        
        return ((((2 * self.level / 5 + 2) * attack.power * self.attack / other.defense) / 50) + 2) * targets * weather * badge * critical * rand * STAB * effectiveness * burn

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
    def __init__(self, pokemon, vs_pokemon, screen_size=100):
        self.screen_size = screen_size
        self._pokemon = pokemon
        self._vs_pokemon = vs_pokemon
        self._name_length = max(len(pokemon.name), len(vs_pokemon.name))
        self._bar_length, self._in_between_length = self._space_constrains()

    def _space_constrains(self):
        columns = 4
        base_space = int(self.screen_size - (self._name_length * 2))
        bar_length = int((base_space * (columns - 1) / columns) / 2)
        in_between_length = int(base_space * 1 / columns)

        if bar_length % 2 == 0: 
            bar_length += 1

        if in_between_length % 2 != 0:
            in_between_length += 1 

        return bar_length, in_between_length

    def health_bar(self, pokemon, fillchar='='):
        health_length = len(str(pokemon.HPpts()))
        max_fill = int((self._bar_length - (health_length * 2) - 3)) # -3 chars from '[ / ]'
        side_fill = int(max_fill / 2)
        fill_with = ceil(pokemon.health() / (pokemon.HPpts() / max_fill))
        fill_with = max_fill if fill_with > max_fill else fill_with

        if fill_with >= side_fill:
            right_fill = ''.rjust((fill_with - side_fill), fillchar)
            fill_with = side_fill
            health = str(pokemon.health()).rjust(health_length, fillchar)
        else:
            right_fill = ''
            health = str(pokemon.health()).rjust(health_length)


        left_fill = fillchar * fill_with 
        left = f'{left_fill:{side_fill}}{health}'
        right = f'{pokemon.HPpts()}{right_fill:{side_fill}}'

        return f'[{left}/{right}]'
    
    def _pokemon_repr(self, pokemon):
        return f'{pokemon.name.capitalize():{self._name_length}} {self.health_bar(pokemon)}'

    def header(self, fillchar='-'):
        vs = "'VS'"
        head = f'{self._pokemon_repr(self._pokemon)}{vs:^{self._in_between_length}}{self._pokemon_repr(self._vs_pokemon)}'
        self.screen_size = len(head)

        system('clear')
        print(f"{fillchar * self.screen_size}\n{head}\n{fillchar * self.screen_size}")
        
    def _get_position(self, position, message_len):
        if position == 'right':
            spaces = int((self.screen_size / 2) + int(self._in_between_length) / 2)
        elif position == 'center':
            spaces = int(self.screen_size / 2) - int(message_len / 2)
        else:
            spaces = 0
            
        return ' ' * spaces
    
    def fancy_message(self, message, pos=None, reverse=False, delay=0.25):
        message_len = len(message)
        position = self._get_position(pos, message_len)
        if reverse:
            for chunk in (message[:i] for i, _ in enumerate(message, start=1)):
                print(f'{position}{chunk:>{message_len}}', end='\r', flush=True)
                sleep(delay)
        else:
            for chunk in (message[:i] for i, _ in enumerate(message, start=1)):
                print(f'{position}{chunk}', end='\r', flush=True)
                sleep(delay)
        
    def screen_message(self, message, pos=None):
        message_len = len(message)
        position = self._get_position(pos, message_len)
        print(f'\n\n{position}{message}', end='')

    def pokemon_moves(self, pokemon, home=False):
        position =  0 if home else int((self.screen_size / 2) + int(self._in_between_length) / 2)
        for i, attack in enumerate(pokemon.moves, start=1):
            print(f'{"".rjust(position)}[{i}.] {attack.name.capitalize()}')



def custom_input(iterable, message):
    while True:
        try:
            user_selection = int(input(f'{message.capitalize()} : '))
            if 0 < user_selection <= len(iterable):
                item = iterable[user_selection - 1]
                break
        except KeyboardInterrupt:
            exit(0)
        except:
            continue
    return item

def get_fighters(pokemons):
    for i, poke in enumerate(pokemons, start=1):
        print(f'[{i}] {poke.name.capitalize()}')

    user_pokemon = custom_input(pokemons, 'choose pokemon')
    pokemons.remove(user_pokemon)
    return user_pokemon, random.choice(pokemons)

if __name__ == '__main__':
    # TODO screen_size (-s), pokemon_limit (-p), moves_limit (-v) by argv
    
    print('Generating pokemons...')
    pokemons = list(PokeGenerator(pokemon_limit=6, moves_limit=10).pokemons)

    while True:
        system('clear')
        pokemons_cp = pokemons.copy()
        user_pokemon, IA_pokemon = get_fighters(pokemons_cp) 
        turn = random.choice((True, False))
        
        screen = Screen(user_pokemon, IA_pokemon)
        
        while user_pokemon.is_alive() and IA_pokemon.is_alive():
            system('clear')
            screen.header()
            
            pokemon, vs_pokemon = (user_pokemon, IA_pokemon) if turn else (IA_pokemon, user_pokemon)
            screen.pokemon_moves(pokemon, home=turn)
            
            if turn:
                attack = custom_input(pokemon.moves, 'choose attack')
            else:
                attack =  random.choice(pokemon.moves)

            message = f'{pokemon.name.capitalize()} attacks {vs_pokemon.name.capitalize()} with {attack.name.capitalize()}'
            screen.fancy_message(message, pos='center', delay=0.05, reverse=not turn)
            pokemon.charge(vs_pokemon, attack)

            turn = not turn
            sleep(1.3)

        system('clear')
        screen.header()
            
        winner = IA_pokemon if IA_pokemon.is_alive() else user_pokemon
        message = f'{winner.name} wins!!!!'.upper()
        screen.fancy_message(message, pos='center', reverse=turn)
        IA_pokemon.recover()
        user_pokemon.recover()
        screen.screen_message('Another Battle (y/n)?: ', pos='center')
        repeat = input()
        if repeat.lower() == 'n':
            break
