# library contains a kiosk and a dictionary of item dictionaries
# item dictionaries contains misc, books, dvd dictionaries
# books contains fiction, non-fiction dictionaries
# fictions contains kids, graphic-novels, novels dictionaries

from collections import OrderedDict
from item_storage import Book, DVD, Misc

class Book_storage(OrderedDict): # key will be item name, value will be frequency
    pass

class DVD_storage(OrderedDict):
    def checkout(): # try to reduce frequency, if it does not work then throw exception for checked out
        return

class Misc_storage(OrderedDict):
    pass

class Library: # generate reports
    books: Book_storage
    DVDs : DVD_storage
    misc : Misc_storage
    patrons : set
    librarians : set