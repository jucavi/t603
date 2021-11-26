from datetime import datetime

calculator = {
    'add': lambda x, y: x + y,
    'substract': lambda x, y: x - y,
    'square': lambda x: x**2,
    'cube': lambda x: x**3,
    'pi': 3.14
}

# print('3 + 5 =', calculator['add'](3, 5))
# print('3 - 5 =', calculator['substract'](3, 5))
# print('3^2   =', calculator['square'](3))
# print('3^3   =', calculator['cube'](3))

start_with = 'm'
lista = ["Marcelo", "Pedro", "German", "Alicia", "María", "Eusebio", "Rolando"]
lista_f = filter(lambda x: x.lower().startswith(start_with), lista)
print(list(lista_f))

a = [1,2,3,4]
b = [5,6,7,8]
multi_m = list(map(lambda x, y: x * y, a, b))
multi_c = list((x * y for x, y in zip(a, b)))
print(multi_m)
print(multi_c)