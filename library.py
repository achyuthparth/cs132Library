# library contains a kiosk and a dictionary of item dictionaries
# item dictionaries contains misc, books, dvd dictionaries
# books contains fiction, non-fiction dictionaries
# fictions contains kids, graphic-novels, novels dictionaries

from item_storage import Book

class Book_storage(dict): # key will be item name, value will be frequency
    pass

class Library: # generate reports
    books: Book_storage
    patrons : set
    librarians : set