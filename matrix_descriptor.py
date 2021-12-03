import numpy as np

class Descriptior:
    def __init__(self, instance):
        self.values = list(map(lambda row: list(row), zip(*instance.matrix)))
        print(self.values)

    def __get__(self, instance, owner):
        print('In __get__')
        return self.values
        
    def __set__(self, instance, value):
        print('In __set__', self)
        print('In __set__', instance.__repr__())
        print(value)

class Matrix:
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.__columns = Descriptior(self)
        
    def rows(self):
        return self.matrix
    
    def columns(self):
        return self.__columns.values
    
    def __str__(self):
        rep = ['[\n'] + [('  ' + str(row) + '\n') for row in self.matrix] + [']\n']
        return ''.join(rep)
        
        
    
matrix = Matrix([[1,2,3], [4,5,6]])

matrix.rows()[1][1] = 8
assert matrix.rows()[1][1] == 8

matrix.columns()[1][1] = 5
assert matrix.columns()[1][1] == 5
