from item_storage import Book
from users import Patron, Librarian
from library import Library
import datetime
from transaction import Transaction_Store, Transaction

class Not_Book(TypeError): pass
class Not_Patron(TypeError): pass
class Kiosk:
    transaction_store : Transaction_Store
    def __init__(self, transaction_store):
        self.transaction_store = transaction_store    

    def checkout_item(self, item, customer): 
# Validate item and customer
        if not(isinstance(item, Book)):
            return Not_Book
        if not(isinstance(customer, Patron)):
            return Not_Patron
# create new transaction
        new_transaction = Transaction(customer.id, item.id)
        self.transaction_store.add_transaction(new_transaction)
        receipt = f"{new_transaction.item_id} {new_transaction.customer_id} {new_transaction.checkout_date}"
# remove the book from the item storage
        return receipt
    
    def checkout_item2(self, item, customer): # built for testing transaction file services
        new_transaction = Transaction(customer.id, item.id)
        self.transaction_store.add_transaction(new_transaction)
        receipt = f"{new_transaction.item_id} {new_transaction.customer_id} {new_transaction.checkout_date}"
        return receipt
        
    def return_item(self, receipt): # handle edge cases, compute fines
        transaction = self.transaction_store.find_transaction(receipt)
        transaction.return_date = datetime.datetime.utcnow()
        return f"{receipt} {transaction.return_date}"
        self.transaction_store.save_to_store()
class Customer_kiosk(Kiosk): pass
class Librarian_Kiosk(Kiosk): pass