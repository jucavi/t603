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
SCREEN_WIDTH = 120
FILL_CHAR = '-'
genres = ["Narrativa extranjera", "Divulgación científica", "Narativa policíaca", "Ciencia ficción", "Autoayuda"]
patrones_de_busqueda = {f'{i}': f'{k}' for i, k in enumerate(DB[0], 1)}

def print_wrap(text, width=SCREEN_WIDTH, fill=' '):
    for line in text.split('\n'):
        if line:
            print(line.center(width, fill))
        else:
            print()

       
def prompt(str_prpmpt=PROMPT):
    return input(str_prpmpt)


# def id_shapes_str():
#     id_shapes = []
    
#     genres_list = (genre.split(' ') for genre in genres)
    
#     for words in genres_list:
#         if len(words) == 1:
#             chars = words[0][0].lower() * 2  
#         elif len(words) > 1:
#             chars = ''.join(word[0].lower() for word in words)            
        
#         id_shapes.append(f'{chars}_(n)')
        
#     return ' '.join(id_shapes) + '\n'


def find_by_user_value(db, key, user_value):
    return [book for book in db if (book.get(key) == user_value) or (user_value.lower() in book.get(key).lower()) ]


def user_value_format(user_value, key):
    if key == 'author':
        user_value = user_value.title()
    elif key == 'title' or key == 'genre':
        user_value = user_value.capitalize()
    else:
        user_value = user_value.lower()
        
    return user_value


def search(db, key):
    text = f'\n"{key.capitalize()}" a buscar'
    print_wrap(text, fill=FILL_CHAR)
    
    user_value = prompt()
    user_value = user_value_format(user_value, key)
        
    books = find_by_user_value(db, key, user_value)
    
    if not books:
        print(f'No hay resultados para la busqueda. ¿Desea volver a interntarlo? (Y/n)')
        reintentar = prompt().lower()
        
        if reintentar == 'y':
            books.append(*search(DB, key))
        else:
            main()
            
    return books
   
   
def menu(patrones_de_busqueda):
    header = '''Gestion de Libros\n'''
    print_wrap(header, fill=FILL_CHAR)
    sub_header = 'Bienvenid@ a su libreria en casa\nBuscar libros por:\n\n'
    for i, opcion in patrones_de_busqueda.items():
        sub_header += f'[{i}] {opcion.capitalize():9}\n'
    sub_header += '  [5] Listar todo\n'
    sub_header += '[q] Salir    \n'
    print_wrap(sub_header)


def adios():
    print('Gracias por hacer uso de nuestra aplicación.\n')


def alert(n):
    print(f'Esta a punto de eliminar {n} elemento(s). ¿Está seguro? (Y/n)')
    user = prompt()
    if user.lower() == 'y':
        return True
    return False


def remove(db, book):
    if alert(1):
        db.remove(book)
        print('Libro Eliminado.')
    
# def remove_all(db, books):
#     if alert(len(books)):
#         for book in books:
#             remove(db, book)


def update(book):
    print('Si desea modificar entre el <nuevo> valor sino pulse <intro>')
    for key, value in book.items():
        print(f'{key}: {value}')
        new_value = prompt()
        if new_value:
            book[key] = new_value
            
            
def show_books(books):
    print_wrap('Listado de Libros', fill=FILL_CHAR)
    print_wrap('''\n{:4}  {:35} {:25} {:25}\n\n'''.format('','Titulo', 'Autor', 'Género'), )
    for i, book in enumerate(books, 1):
        print_wrap(f'''{i:4}. {book['title']:35} {book['author']:25} {book['genre']:25}\n''')

def create_update_delete_menu(db, books):
    print_wrap('\n\nCrear(C) Editar(E) Borrar(B)')

    user_action = prompt()
    if len(user_action) > 1:
        action, book_id = user_action[0], user_action[1]
        
        # los libroso son mostrados [index + 1] en el menu de show_books
        book_id = int(book_id) - 1
        action = action.lower()
        
        if book_id in range(len(books)):
            if action == 'b':
                remove(db, books[book_id])
            elif action == 'e':
                update(books[book_id])
            else:
                print('La acción no existe o aun no se ha implementado' )
    elif user_action:
        print('Formato de comando erroneo')
            
    main()
    
def main():
    while True:
        menu(patrones_de_busqueda)
        user_input = prompt()
        
        if user_input.lower() == 'q':
            adios()
            exit()
        
        if user_input in patrones_de_busqueda:
            books = search(DB, patrones_de_busqueda[user_input])
            show_books(books)
            create_update_delete_menu(DB, books)
        elif user_input == '5':
            books = DB
            show_books(books)
            create_update_delete_menu(DB, books)
        else:
            print('Por favor introduzca una opción válida, pulse cualquier tecla para contiuar')

main()