from item_storage import Book, DVD, Misc
from users import Patron, Librarian
from library import Library
import datetime




class Kiosk:
    def __init__(self, transaction_store):
        self.transaction_store = transaction_store
    
    def checkout_item(self, item, customer): 
# Validate item and customer
# create new transaction
        new_transaction = Transaction(customer.id, item.id)
        self.transaction_store.save_transaction(new_transaction)
        
    def return_item(self, item): # handle edge cases, compute fines
        transaction = self.transaction_store.find_transaction(item.id)
        transaction.return_date = datetime.UTC
        self.transaction_store.save_to_store()

class Customer_kiosk(Kiosk):
    
    @classmethod
    def checkout_item(cls, item, customer):
        super().checkout_item(item)    

class Librarian_kiosk(Kiosk):
    
    @classmethod
    def add_item(cls, item, customer):
        super().item_insert(item)
            
    @classmethod
    def add_patron(cls, name, email, number, id):
        new_patron = Patron(name, email, number, id)
        
class Transaction:
    customer_id : int
    item_id : str
    checkout_date : str # figure this out later
    return_date : str
    fine : float
    
    def __init__(self, customer_id, item_id):
        self.customer_id = customer_id
        self.item_id = item_id
        self.checkout_date = datetime.UTC

class Transaction_Store:
    
    def add_transaction(self, transaction):
        pass

    def find_transaction(self, item_id):
        pass
    
    def save_to_store(self):
        pass
    
class Transaction_File(Transaction_Store):
    
    def __init__(self, file_name):
        self.file_name = file_name
    
    def add_transaction(self, transaction):
        pass

    def find_transaction(self, item_id):
        pass
    