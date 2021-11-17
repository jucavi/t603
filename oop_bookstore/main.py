from book import Book
from data_store import DataStore
from data_manager import Manager

mg = Manager('books.pckl', __file__)
ds = DataStore(mg.load())

print(ds.books)

ds.find_book_by_isbn()