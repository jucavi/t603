# pwd = 'pastTTTdÑ45'

# if len(pwd) >= 8 and pwd.isalnum() and not pwd.isnumeric() and not pwd.isalpha() and pwd.lower() != pwd and pwd.upper() != pwd:
#     print('Contraseña correcta')
    
# a = "murcielago"

# Considerando la variable a:
# Reemplazar todas las vocales con el siguiente esquema:
# a: 2,
# e: 4,
# i: 8,
# o: 16, 
# u: 32

# a = a.replace('a', '2')
# a = a.replace('e', '4')
# a = a.replace('i', '8')
# a = a.replace('o', '16')
# a = a.replace('u', '32')

# print(a)

# vowels = {
#     'a': '2',
#     'e': '4',
#     'i': '8',
#     'o': '16', 
#     'u': '32'
# }
# a = "murcielago"

# for vowel, value in vowels.items():
#     a = a.replace(vowel, value)

# print(a)

# Agregar a la variable a el texto "kwargs" por cada caracter que la palabra tenga (se considera cualquier tipo de caracter)
# Si el resultado tiene como longitud una cantidad impar de caracteres, obtener el caracter que se encuentra en el medio

# b = 75

# Si es par, agregar la variable b al final

# b = 75

# a += 'kwargs' * len(a)

# if len(a) % 2 == 0:
#     a += str(b)
# else:
#     a = a[len(a)//2]

########################## clase 3 ##################################

# import random

# options = ['rock', 'paper', 'scissors']

# count = 0
# while count < 3:
#     user = input('Choice [rock, paper, scissors]: ')
#     user = user.lower()
    
#     pc = random.choice(options)
#     if user in options:
#         # Reahacer con index()
#         win_condition = (user == 'rock' and pc == 'scissors') or (user == 'paper' and pc == 'rock') or (user == 'scissors' and pc == 'paper')

#         if user == pc:
#             print('Tie')             
#         elif win_condition:
#             print('Win')   
#         else:
#             print('Lose')
    
#         print()
#         count += 1
#     else:
#         print('Invalid choice')

# print('Bye!')
