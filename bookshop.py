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

genre = ["Narrativa extranjera", "Divulgación científica", "Narativa policíaca", "Ciencia ficción", "Autoayuda"]

def menu():
    print('Welcome'.center(30, '-'))
    
def alert(n):
    user = input(f'\t\tEsta a punto de eliminar {n} elemento(s). ¿Está seguro? (Y/n): ')
    if user.lower() == 'y':
        return True
    return False
    
def find_by(db, key, value):
    return [book for book in db if book.get(key) == value]

def remove(db, key, value):
    books_found = find_by(db, key, value)
    if len(books_found) > 1:
        return None
    if alert(len(books_found)):
        db.pop(books_found[0])
    
def remove_all(db, key, value):
    books_found = find_by(db, key, value)
    if alert(len(books_found)):
        for book in books_found:
            db.pop(book)
    
  
while True:
    menu()
    user = input('')
    
# Librería

# Gestiona una librería virtual

# Podrá buscar libros por los siguientes parámetros:

#     id
#     Autor
#     Título
#     Genero

# Ademas, se podrá modificar los datos de cada uno de los libros así como eliminarlos

