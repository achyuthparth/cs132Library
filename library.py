# library contains a kiosk and a dictionary of item dictionaries
# item dictionaries contains misc, books, dvd dictionaries
# books contains fiction, non-fiction dictionaries
# fictions contains kids, graphic-novels, novels dictionaries


from kiosk import Kiosk
from item_storage import Book, DVD, Misc
from collections import OrderedDict

class Book_storage(OrderedDict):
    pass
# key will be item name, value will be frequency

class DVD_storage(OrderedDict):
    pass

class Misc_storage(OrderedDict):
    pass


class Library:
    books: Book_storage
    DVDs : DVD_storage
    misc : Misc_storage
    
    def __init__(self, books, DVDs, misc):
        pass
    
    @staticmethod
    def checkout(item):
        if type(item) == Book:
            Kiosk.book_checkout(item)
        if type(item) == DVD:
            Kiosk.DVD_checkout(item)
        if type(item) == Misc:
            Kiosk.misc_checkout(item)
            
    @staticmethod
    def add_item(item):
        if type(item) == Book:
            Kiosk.book_insert(item)
        if type(item) == DVD:
            Kiosk.DVD_insert(item)
        if type(item) == Misc:
            Kiosk.misc_insert(item)