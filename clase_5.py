import timeit

m_course = [{
	"name": "Patricia",
	"id" :  "001",
    "score": 8.1
},
{
	"name": "Nicole",
	"id" :  "002",
    "score": 6.6
},
{
	"name": "Javier",
	"id" :  "003",
    "score": 10
},
{
	"name": "Verónica",
	"id" :  "004",
    "score": 8.6
},
{
	"name": "Guillermo",
	"id" :  "005",
        "score": 4
},
{
	"name": "Pablo",
	"id" :  "006",
    "score": 9
},
{
	"name": "Patricia",
	"id" :  "007",
    "score": 2.3
}]

a_course =[
{
	"name": "Germán",
	"id" :  "001",
    "score": 6.8
},
{
	"name": "Sara",
	"id" :  "002",
    "score": 8.8
},
{
	"name": "Jorge",
	"id" :  "003",
    "score": 3.3
},
{
	"name": "María",
	"id" :  "004",
    "score": 9.8
},
{
	"name": "Alicia",
	"id" :  "005",
    "score": 5.6
},
{
	"name": "Hernesto",
	"id" :  "006",
    "score": 6.8
}]


    # Obtener la nota de Hernesto
    
student_to_find = 'Hernesto'
courses = a_course + m_course

for student in a_course:
    if student['name'].lower() == student_to_find.lower():
        print(student['score'])

print()

    # Cuántos estudiantes tienen un nombre que empiece por la letra "P"

count = 0
for student in courses:
    if student['name'].lower().startswith('p'):
        count += 1
        
print(f'{count} persona(s) comieza su nombre por la letra "P"')
print()

    # Nombre de el/la estudiante con la nota más alta

max_score = 0
student_max_score = []
for student in courses:
    if student['score'] == max_score:
        student_max_score.append(student['name'])
        
    elif student['score'] > max_score:
        max_score = student['score']
        student_max_score = [student['name']]
        
print(f'Best score: {student_max_score}\n')

students_by_scores = {}
for student in courses:
    if students_by_scores.get(student['score']):
        students_by_scores[student['score']].append(student['name'])
    else:
        students_by_scores[student['score']] = [student['name']]
    

print('Mejor nota:', students_by_scores[max(students_by_scores)])
print('Peor nota: ', students_by_scores[min(students_by_scores)])
print()
print(students_by_scores)
print()
 
    # [idem] más baja
    
min_score = 11
student_max_score = None
for student in courses:
    if student['score'] < min_score:
        min_score = student['score']
        student_min_score = student
        
print(f'Worst score: {student_min_score["name"]}')  
print()

    # Modificar la nota de Alica a --> 6.7

student_to_find = 'alicia'
new_score = 6.7
for student in a_course:
    if student['name'].lower() == student_to_find:
        print('Score antes de modificar: ', student)
        student['score'] = new_score
        print('Score despues de ser modificado:', student)
        
print()

    # Agregar a los estudiantes de la lista m_course la letra "M" por delante de cada ID --> M006
for student in a_course:   
    student['id'] = 'A' + student['id']

print(a_course[-1])
print()

for student in m_course:   
    student['id'] = 'M' + student['id']

print(m_course[-1])
print()

    # Crear dos listas, una con los estudiantes suspensos y otra con los estudiantes aprobados (6)
    
suspensos = []
aprovados = []

for student in courses:
    if student['score'] < 6:
        suspensos.append(student)
    else:
        aprovados.append(student)
        
print('Aprovados:', aprovados)
print('Suspensos:', suspensos)
print()

suspensos = list(map(lambda x: x['name'], filter(lambda x: x['score'] < 6, courses)))
aprovados = list(map(lambda x: x['name'], filter(lambda x: x['score'] >= 6, courses)))

print('Aprovados:', aprovados)
print('Suspensos:', suspensos)
print()

def test():
    suspensos = []
    aprovados = []

    for student in courses:
        if student['score'] < 6:
            suspensos.append(student['name'])
        else:
            aprovados.append(student['name'])
            
for_loop_time =  timeit.timeit("test()", globals=locals())
print('for loop execution 1 Million times: ', for_loop_time)

def test():
    list(map(lambda x: x['name'], filter(lambda x: x['score'] < 6, courses)))
    list(map(lambda x: x['name'], filter(lambda x: x['score'] >= 6, courses)))

map_filter_time_2x = timeit.timeit("test()", globals=locals())
print('map-filter execution 1 Million times:', map_filter_time_2x, '\n\n')

print('for loopt', map_filter_time_2x / for_loop_time, ' times faster than map-filter')