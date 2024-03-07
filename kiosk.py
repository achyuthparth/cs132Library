from item_storage import Book, Book_Storage
from users import User, User_Storage
from library import Library
import datetime
from transaction import Transaction_Store, Transaction
from admin import Roles_Store

class Not_Book(TypeError): pass
class Not_User(TypeError): pass
class Not_Librarian(TypeError): pass
class Kiosk: # add methods for checking permissions
    transaction_store : Transaction_Store
    role_store : Roles_Store # dependency injection
    book_store : Book_Storage
    user_store : User_Storage
    def __init__(self, transaction_store, role_store, book_store, user_store):
        self.transaction_store = transaction_store
        self.role_store = role_store
        self.book_store = book_store
        self.user_store = user_store

    def check_permissions(self, user, permission):
        user_role_list = user.roles
        for role in user_role_list:
            if permission in self.role_store[role]:
                return True
        return False

    def checkout_item(self, item, user):
# Validate item and customer type
        if not(isinstance(item, Book)):
            return Not_Book
        if not(isinstance(user, User)):
            return Not_User
# validate if user has permissions
        if not(self.check_permissions(user, "checkout_books")):
            raise PermissionError("Does not have permission to checkout books")
# create new transaction
        new_transaction = Transaction(user.id, item.id)
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
        self.transaction_store.write_file()
        return f"{receipt} {transaction.return_date}"
class Customer_kiosk(Kiosk): pass
class Librarian_Kiosk(Kiosk): pass