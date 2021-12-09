class Book:
    def __init__(self, isbn, title, author, genre):
        self.isbn = isbn.upper()
        self.title = title.title()
        self.author = author.title()
        self.genre = genre.title()
    
    def __str__(self):
        return f'{self.isbn} {self.title} by {self.author}, genre: {self.genre}'
    
    def include(self, pattern):
        pattern = pattern.lower()
        
        if pattern in self.title.lower() \
            or pattern in self.author.lower() \
            or pattern in self.genre.lower():
                
            return True
        return False
    
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.__dict__.keys():
                self.__setattr__(attr, value)
            else:
                raise AttributeError(f'{attr}: Is not valid Attribute')