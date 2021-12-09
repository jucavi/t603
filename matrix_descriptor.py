import numpy as np

class Descriptor:
    def __init__(self, obj):
        self.col = list(map(lambda row: list(row), zip(*obj.matrix)))
        
    def __get__(self, obj, objtype=None):
        print('In __get__')
        return self.col
        
    def __set__(self, obj, value):
        print('In __set__')
     
    def __str__(self):
        return str(self.col)

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.col = Descriptor(self)
        
    def rows(self):
        return self.matrix
    
    def columns(self):
        return self.col
    
    def __str__(self):
        rep = ['[\n'] + [('  ' + str(row) + '\n') for row in self.matrix] + [']\n']
        return ''.join(rep)
        
        
    
matrix = Matrix([[1,2,3], [4,5,6]])

rows = matrix.rows()
rows[1][1] = 8
assert matrix.rows()[1][1] == rows[1][1]

columns = matrix.columns()
print(type(columns))
columns[1][1] = 5


print(matrix.rows())
print(matrix.columns())
