from item_storage import Book, DVD, Misc
from users import Patron, Librarian
from library import Library

class Kiosk:
    
    @staticmethod
    def checkout(cls, item):
        if type(item) == Book:
            Library.book_checkout(item)
        if type(item) == DVD:
            Library.DVD_checkout(item)
        if type(item) == Misc:
            Library.misc_checkout(item)
    
    @staticmethod
    def book_checkout(item):
        return
    
    @staticmethod
    def DVD_checkout(item):
        return
    
    @staticmethod
    def misc_checkout(item):
        return
    
    @staticmethod
    def book_insert(item):
        return
    
    @staticmethod
    def DVD_insert(item):
        return
    
    @staticmethod
    def misc_insert(item):
        return

class Customer_kiosk(Kiosk):
    
    @classmethod
    def checkout(cls, item):
        if type(item) == Book:
            super().book_checkout(item)
        if type(item) == DVD:
            super().DVD_checkout(item)
        if type(item) == Misc:
            super().misc_checkout(item)
            
class Librarian_kiosk(Kiosk):
    
    @classmethod
    def add_item(cls, item):
        if type(item) == Book:
            super().book_insert(item)
        if type(item) == DVD:
            super().DVD_insert(item)
        if type(item) == Misc:
            super().misc_insert(item)
            
    @classmethod
    def add_patron(cls, name, email, number, id):
        new_patron = Patron(name, email, number, id)