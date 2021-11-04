DB = [{
    "id": "cf_1",
    "title": "El hombre bicentenario",
    "author": "Isaac Asimov",
    "genre": "Ciencia ficción"
},
{
    "id": "ne_1",
    "title": "Lobo de mar",
    "author": "Jack London",
    "genre": "Narrativa extranjera"
},
{
    "id": "np_1",
    "title": "El legado de los huesos",
    "author": "Dolores Redondo",
    "genre": "Narrativa policíaca"
},
{
    "id": "dc_1",
    "title": "El error de Descartes",
    "author": "Antonio Damasio",
    "genre": "Divulgación científica"
},
{
    "id": "dc_2",
    "title": "El ingenio de los pájaros",
    "author": "Jennifer Ackerman",
    "genre": "Divulgación científica"
},
{
    "id": "ne_1",
    "title": "El corazón de las tinieblas",
    "author": "Joseph Conrad",
    "genre": "Narrativa extranjera"
},
{
    "id": "dc_5",
    "title": "Metro 2033",
    "author": "Dmitri Glujovski",
    "genre": "Divulgación científica"
},
{
    "id": "dc_5",
    "title": "Sidharta",
    "author": "Hermann Hesse",
    "genre": "Narrativa extranjera"
},
{
    "id": "el_1",
    "title": "Andres Trapiello",
    "author": "Las armas y las letras",
    "genre": "Narrativa extranjera"
},
{
    "id": "aa_1",
    "title": "El poder del ahora",
    "author": "Ekhart Tolle",
    "genre": "Narrativa extranjera"
},
]

PROMPT = '>> '
genres = ["Narrativa extranjera", "Divulgación científica", "Narativa policíaca", "Ciencia ficción", "Autoayuda"]

def prompt(str_prpmpt=PROMPT):
    return input(str_prpmpt)


def id_shapes_str():
    id_shapes = []
    
    genres_list = (genre.split(' ') for genre in genres)
    
    for words in genres_list:
        if len(words) == 1:
            chars = words[0][0].lower() * 2  
        elif len(words) > 1:
            chars = ''.join(word[0].lower() for word in words)            
        
        id_shapes.append(f'{chars}_(n)')
        
    return ' '.join(id_shapes) + '\n'


def find_by_user_value(db, key, user_value):
    return [book for book in db if book.get(key) == user_value]

def user_value_format(user_value, key):
    if key == 'author':
        user_value = user_value.title()
    elif key == 'title' or key == 'genre':
        user_value = user_value.capitalize()
    else:
        user_value = user_value.lower()
        
    return user_value

def search(db, key):
    print(f' "{key.capitalize()}" a buscar '.center(50, '-') + '\n')
    
    user_value = prompt()
    user_value = user_value_format(user_value, key)
        
    books = find_by_user_value(db, key, user_value)
    
    if not books:
        print(f'No hay resultados para la busqueda. ¿Desea volver a interntarlo? (Y/n)')
        reintentar = prompt().lower()
        
        if reintentar == 'y':
            search(DB, key)
            
    return books
   
   
def menu():
    print(' Gestion de Libros '.center(50, '-'))
    print(
'''
        Bienvenid@ a su libreria en casa

            Buscar libros por:
    
                [1]   Id
                [2]   Título
                [3]   Autor
                [4]   Género
                [Q]   Salir 
''')


def adios():
    print('Gracias por hacer uso de nuestra aplicación.\n')


def alert(n):
    user = input(f'\t\tEsta a punto de eliminar {n} elemento(s). ¿Está seguro? (Y/n): ')
    if user.lower() == 'y':
        return True
    return False


def remove(db, book):
    db.remove(book)

    
def remove_all(db, books):
    if alert(len(books)):
        for book in books:
            db.remove(book)


def update(db, book):
    for key, value in book.items():
        new_value = input(f'{key}: {value} Si desea modificarlo entre el nuevo valor sino pulse Enter: ')
        if new_value:
            book[key] = new_value

def main():
    while True:
        menu()
        user_input = prompt()
        
        patrones_de_busqueda = {'1': 'id', '2': 'title', '3': 'author', '4': 'genre'}
        
        if user_input.lower() == 'q':
            adios()
            break
        
        if user_input in patrones_de_busqueda:
            books = search(DB, patrones_de_busqueda[user_input])
            show_books(books)
            create_update_delete_menu()
        else:
            input('Por favor introduzca una opción válida, pulse cualquier tecla para contiuar')

