class DataStore:
    def __init__(self, books):
        """DataStore object 

        Args:
            books (list): A list of Books
        """ 
        self.books = books
        
    def add_book(self, book):
        """Add book to DataStore

        Args:
            book (Book): An instance of Book
        """
        self.books.append(book)

     
    def add_books(self, books_list):
        """Add books to DataStore

        Args:
            books_list (list): A list of Book instances
        """
        try:
            for book in books_list:
                self.add_book(book)
        except Exception as e:
            print(e)


    def find_book_by_isbn(self, isbn):
        """Find a book by isbn

        Args:
            isbn (str): ISBN 

        Returns:
            [Book]: if book with isbn exist in DataStore, [None] if not exist
        """
        isbn = isbn.upper()
        
        if self.books:
            for book in self.books:
                if book.isbn == isbn:
                    return book
        else:
            return None
        
        
    def find_books_with(self, pattern):
        """Finds all books that [pattern] appear in author, title or genre

        Args:
            pattern (str): Pattern to match

        Returns:
            [list]: A list of books
        """
        return [book for book in self.books if book.include(pattern)]
    
    def remove_book(self, book):
        self.books.remove(book)
        
    def show_all(self):
        for book in self.books:
            print(book)
            
        