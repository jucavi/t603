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
LINES_PER_PAGE = 5
BOOK_KEYS = ['id', 'title', 'author', 'genre']
genres = ["Narrativa extranjera", "Divulgación científica", "Narativa policíaca", "Ciencia ficción", "Autoayuda"]
patrones_de_busqueda = {f'{i}': f'{k}' for i, k in enumerate(BOOK_KEYS, 1)}

def print_wrap(text, width=SCREEN_WIDTH, fill=' '):
    for line in text.split('\n'):
        if line:
            print(line.center(width, fill))
        else:
            print()

       
def prompt(str_prompt=PROMPT):
    return input(str_prompt)


def id_generator(db, genre):
    words = genre.split(' ')
    if len(words) == 1:
        chars = words[0][0].lower() * 2  
    elif len(words) > 1:
        chars = ''.join(word[0].lower() for word in words[:2])
        
    if not chars:
        chars = '##'
        
    id_partial = f'{chars}_'
    
    books_by_genre = find_by_user_value(db, 'id', id_partial)
    try:
        max_id = max(int(book['id'][3:]) for book in books_by_genre)
    except :
        max_id = 0
     
    return id_partial + str(max_id + 1)


def is_valid_id(db, book, id_candidate):
    unique = filter(lambda b: (b != book) and (b['id'] != id_candidate), db)
    true_format = id_candidate[:3] == id_generator(db, book['genre'])[:3]
    
    return unique and true_format


def find_by_user_value(db, key, user_value):
    try:
        return [book for book in db if (book.get(key) == user_value) or (user_value.lower() in book.get(key).lower()) ]
    except:
        return []


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
        message = f'No hay resultados para la busqueda. ¿Desea volver a interntarlo? (Y/n)'
        prompt_message = PROMPT.rjust(SCREEN_WIDTH // 3)

        if alert(message, prompt_message):
            books.extend(search(DB, key))
        else:
            main(db)
            
    return books
   
   
def menu(patrones_de_busqueda):
    header = '''Gestion de Libros\n'''
    print_wrap(header, fill=FILL_CHAR)
    sub_header = 'Bienvenid@ a su libreria en casa\nBuscar libros por:\n\n'
    for i, opcion in patrones_de_busqueda.items():
        sub_header += f'[{i}] {opcion.capitalize():9}\n'
    sub_header += '  [L] Listar todo\n'
    sub_header += '  [C] Crear libro\n'
    sub_header += '[q] Salir    \n'
    print_wrap(sub_header)


def adios():
    print('Gracias por hacer uso de nuestra aplicación.\n')


def alert(message='Alerta!', prompt_message=PROMPT):
    print_wrap(message)
    user = prompt(prompt_message)
    
    if user.lower() == 'y':
        return True
    return False


def remove(db, book):
    message = f'''Esta a punto de eliminar "{book["title"].upper()}". ¿Está seguro? (Y/n)'''
    prompt_message = PROMPT.rjust(SCREEN_WIDTH // 3)
    
    if alert(message, prompt_message):
        db.remove(book)
        print_wrap('Libro Eliminado\n\n', fill='*')


def update(db, book):
    print_wrap('Si desea modificar entre el <NUEVO> valor sino pulse <INTRO>\n', fill=FILL_CHAR)
    for key, value in book.items():
        if key != 'id':
            new_value = prompt(str_prompt=f'{key}: {value} >> '.rjust(SCREEN_WIDTH // 3))
           
            if new_value:
                #quedaria mejor si fuese en ingles
                message = f'¿Desea modificar el {key.capitalize()} {value.title()} por {new_value.title()} (Y/n)?'
                prompt_message = PROMPT.rjust(SCREEN_WIDTH // 3)
                
                if alert(message, prompt_message):
                    book[key] = user_value_format(new_value, key)
                
    genre = book['genre']
    if genre and (genre not in genres):
        genres.append(genre)

    print_wrap('Si la ID no es correcta será generada automaticamente', fill=FILL_CHAR)
    new_id = prompt(str_prompt=f'id: {book["id"]} >> '.rjust(SCREEN_WIDTH // 3))
    new_id = user_value_format(new_id, 'id')
    
    if is_valid_id(db, book, new_id):
        book['id'] = new_id
    else:
        book['id'] = id_generator(db, book['genre'])
     
            
def show_books(books):
    print_wrap('Listado de Libros', fill=FILL_CHAR)
    BOOKS_HEADER = '''\n{:4}  {:4}\t{:40} {:35} {:25}\n\n'''.format('', *(key.upper() for key in BOOK_KEYS))
    print_wrap(BOOKS_HEADER)
    pag = 1
    for i, book in enumerate(books, 1):
        print_wrap(f'''{i:4}. {book['id']}\t{book['title']:40} {book['author']:35} {book['genre']:25}\n''')
        # Algun tipo de paginación
        if i % LINES_PER_PAGE == 0:
            print_wrap(f'({pag})', fill=FILL_CHAR)
            prompt(str_prompt=': ')
            if i != len(books): 
                print_wrap(BOOKS_HEADER)
                pag += 1
    if not len(books) % LINES_PER_PAGE == 0:
        print_wrap(f'({pag})', fill=FILL_CHAR)
        prompt(str_prompt=': ')
    
    
def create(db):
    print_wrap('Nuevo Libro\n\n', fill=FILL_CHAR)
    while True:
        new_book = {}
        for key in BOOK_KEYS[1:]:
            value = prompt(str_prompt=f'{key}: '.rjust(SCREEN_WIDTH // 3))
            value = user_value_format(value, key)
            new_book[key] = value
            
        new_book['id'] = id_generator(db, new_book['genre'])
        db.append(new_book)
        print_wrap('\nNuevo libro agregado a la biblioteca\n', fill=FILL_CHAR)
        
        message = f'¿Desea crear otro libro? (Y/n)'
        prompt_message = PROMPT.rjust(SCREEN_WIDTH // 3)
        
        if alert(message, prompt_message):
            create(db)  
        else:
            main(db)
         

def create_update_delete_menu(db, books):
    print_wrap('\n\nCrear(C) Editar(E) Borrar(B) Inicio(I)')
    print_wrap('Ej. B2, E1')

    user_action = prompt().lower()
    if len(user_action) > 1:
        action, book_id = user_action[0], user_action[1:] 
        # los libros son mostrados [index + 1] en el menu de show_books
        if book_id.isdigit():
            book_id = int(book_id) - 1
        
            if book_id in range(len(books)):
                if action == 'b':
                    remove(db, books[book_id])
                elif action == 'e':
                    update(db, books[book_id])
                else:
                    print_wrap('La acción no existe o aun no se ha implementado' )
        else:
            print('Formato de comando erroneo')
            
    elif user_action == 'c':
        create(db)
        
    elif user_action and user_action != 'i':
        print('Formato de comando erroneo')     
    main(db)


def main(db):
    while True:
        menu(patrones_de_busqueda)
        user_input = prompt().lower()
        
        if user_input == 'q':
            adios()
            exit()
        
        if user_input in patrones_de_busqueda:
            books = search(db, patrones_de_busqueda[user_input])
            show_books(books)
            create_update_delete_menu(db, books)
        elif user_input == 'l':
            books = db
            show_books(books)
            create_update_delete_menu(db, books)
        elif user_input == 'c':
            create(db)
        else:
            print('Por favor introduzca una opción válida, pulse cualquier tecla para contiuar')


main(DB)