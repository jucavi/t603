import requests

URL = 'https://pokeapi.co/'

class Pokemon:
    def __init__(self, name, element, hp, attacks):
        self.name = name
        self.element = element
        self.hp = hp
        self.atacks = attacks
        
    def learn(self, attack):
        self.attacks.append(attack)
        
    def attack(self, other, attack):
        # relacion elementos y self.element ?
        if attack.name in self.attacks:
            other.hp - self.attak.dammage
    
    def receive_damage(self, other_attack):
        # relacion elementos y self.element ?
        self.hp - other_attack.damage
    

class Attack:
    def __init__(self, name, element, damage):
        self.name = name
        self.element = element
        self.dmage = damage
        