from item_storage import Book
from users import Patron, Librarian
from library import Library
import datetime
from transaction import Transaction_Store, Transaction

class Kiosk:
    transaction_store : Transaction_Store
    def __init__(self, transaction_store):
        self.transaction_store = transaction_store    

    def checkout_item(self, item, customer): 
# Validate item and customer
# create new transaction
        new_transaction = Transaction(customer.id, item.id)
        self.transaction_store.add_transaction(new_transaction)
        receipt = f"{new_transaction.item_id} {new_transaction.customer_id} {new_transaction.checkout_date}"
        return receipt
        
    def return_item(self, receipt): # handle edge cases, compute fines
        transaction = self.transaction_store.find_transaction(receipt)
        transaction.return_date = datetime.datetime.utcnow().isoformat()
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