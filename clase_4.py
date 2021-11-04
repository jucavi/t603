# a = [0,2,3,4]
# '''
# CRUD
#     Create
#     Read
#     Update
#     Delete
# '''

# # Create
# a.append(5)
# a.insert(1, 1)

# # Read
# a
# a[2]

# # Update
# a[0] = 1

# # Delete
# a.pop()
# a.clear()
# a.remove(1)


# print(a)


"""
Ejercicios

    Simular los siguientes metodos de listas:

    count
    index

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,98]
"""

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,98]

to_find = 8
count = 0
for number in repeated_numbers:
    if number == to_find:
        count += 1

print(f'{to_find} repeated in {repeated_numbers} {count} times')
        


count = 0
index = 0    
while index < len(repeated_numbers):
    if repeated_numbers[index] == to_find:
        count += 1
    index += 1
       
print(f'{to_find} repeated in {repeated_numbers} {count} times')



index = -1
for i, number in enumerate(repeated_numbers):
    if number == to_find:
        index = i
        break
    
print(f'{to_find} found in {index}')



index = -1
i = 0
while i < len(repeated_numbers):
    if repeated_numbers[i] == to_find:
         index = i
         break
    i += 1
    
print(f'{to_find} found in {index}')


#     Crear otro iterable con valores únicos

set_list = []
for num in repeated_numbers:
    if num not in set_list:
        set_list.append(num)
print(f"Uniques: {set_list}")

i = 0
set_list = []
while i < len(repeated_numbers):
    if repeated_numbers[i] not in set_list:
        set_list.append(repeated_numbers[i])
    i += 1
print(f"Uniques: {set_list}")

set_list = list(set(repeated_numbers))
print(f"Uniques: {set_list}")

#     Ordenar los valores de manera ascendente y descendente

ordered_asc = sorted(repeated_numbers)
ordered_des = sorted(set_list, reverse=True)

print('\t\t     ', ordered_asc)
    # BUBBLE SORT ASC
test_set_list = repeated_numbers.copy()
n = len(repeated_numbers)
for i in range(n):
    for j in range(n-1-i):
        if test_set_list[j] > test_set_list[j + 1]:
            test_set_list[j], test_set_list[j + 1] = test_set_list[j + 1], test_set_list[j]
            
print('Por Bubble Sort ASC: ', test_set_list)
 

print('\t\t     ', ordered_des)
    # BUBBLE SORT DES
test_set_list = set_list.copy()
n = len(set_list)
for i in range(n):
    for j in range(n-1-i):
        if test_set_list[j] < test_set_list[j + 1]:
            test_set_list[j], test_set_list[j + 1] = test_set_list[j + 1], test_set_list[j]
            
print('Por Bubble Sort DES: ', test_set_list)



#     En el mismo bucle crear dos listas, una solo con los valores pares y otra con los impares

odd = []
pair = []
for number in repeated_numbers:
    if number % 2 == 0:
        pair.append(number)
    else:
        odd.append(number)
    
print(f'Odd: {odd}')
print(f'Pair: {pair}')


i = 0
odd = []
pair = []
while i < len(repeated_numbers):
    if repeated_numbers[i] % 2 == 0:
        pair.append(repeated_numbers[i])
    else:
        odd.append(repeated_numbers[i])
    i += 1
    
print(f'Odd: {odd}')
print(f'Pair: {pair}')

#     Crear una lista resultante con los valores de repeated_numbers al cuadrado

squares = [n ** 2 for n in repeated_numbers]
print(squares)

squares = []
for num in repeated_numbers:
    squares.append(num ** 2)

squares = []
i = 0
while i < len(repeated_numbers):
    squares.append(repeated_numbers[i] ** 2)
    i += 1
print(squares)

#     Obtener la media

print(sum(squares) / len(squares))

total = 0
for num in squares:
    total += num
print(total / len(squares))

total = 0
i = 0
while i < len(squares):
    total += squares[i]
    i += 1
print(total / len(squares))

#     Encontrar el valor máximo de la lista y cambiarlo por 1000

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,150,98]
val_max = max(repeated_numbers)
index = repeated_numbers.index(val_max)
repeated_numbers[index] = 1000
print(repeated_numbers)

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,150,98]
repeated_numbers[repeated_numbers.index(max(repeated_numbers))] = 1000
print(repeated_numbers)

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,150,98]
max_num = max(repeated_numbers)
repeated_numbers = list(map(lambda x: 1000 if x == max_num else x, repeated_numbers))
print(repeated_numbers)

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,150,98]
max_num = max(repeated_numbers)
i = 0
while i < len(repeated_numbers):
    if repeated_numbers[i] == max_num:
        repeated_numbers[i] = 1000
    i += 1
print(repeated_numbers)

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,150,98]
max_num = sorted(repeated_numbers)[-1]

for index, num in enumerate(repeated_numbers):
    if num == max_num:
        repeated_numbers[index] = max_num
        
print(repeated_numbers)

#     Obtener la sumatoria de los valores comprendidos entre las posiciones 4 y 9 inclusive

print('Sum:', sum(repeated_numbers[4:10]))

sum = 0
for i, number in enumerate(repeated_numbers):
    if 4 <= i <= 9:
        sum += number
    
print(f'Sum: {sum}')


sum = 0
i = 0
while i < len(repeated_numbers):
    if 4 <= i <= 9:
        sum += repeated_numbers[i]
    i += 1
    
print(f'Sum: {sum}')


# Fibonacci
#     Crea 15 números de la secuenca Fibonacci (1,1,2,3,5,8...)
n = 15
a = 0
b = 1
fib = []
while len(fib) <= n:
    a, b = b, a + b
    fib.append(a)
    
print(f'Fibonacci series for {n} iterations:', fib)


fib = [1,1]
while len(fib) <= n:
    fib.append(fib[-1] + fib[-2])
    
print(f'Fibonacci series for {n} iterations: {fib}')

fib = [1,1]
for _ in range(n-1):
    fib.append(fib[-1] + fib[-2])
    
print(f'Fibonacci series for {n} iterations: {fib}')

#  Encontrar el número maximo  y mínimo en un iterable

repeated_numbers = [1,2,2,10,11,13,2,8,9,16,26,50,51,56,89,150,2,3,6,7,67,150,98]

import math

max_number = -math.inf
for num in repeated_numbers:
    if num > max_number:
        max_number = num
        
print(max_number)

min_number = math.inf
for num in repeated_numbers:
    if num < min_number:
        min_number = num
        
print(min_number)

# Triangulo de Pascal