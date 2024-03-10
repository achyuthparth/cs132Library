# Kiosk will be the logic to handle all the actions internally

from item_storage import Book, Book_Storage, Book_None_Available, Book_Not_Found
from users import User, User_Storage, User_Not_Found, User_Already_Exists
import datetime
from transaction import Transaction_Store, Transaction, No_Transaction_Present
from roles import Roles_Store, Role

class Not_Book(TypeError): pass
class Not_User(TypeError): pass

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
        
    def login(self, user_id):
        # Validate user type
        if not(isinstance(user_id, str)):
            raise TypeError("Enter a string for user ID")
        
        # Check if user exists, and if not return exceptions
        try: return self.user_store.find_user_id(user_id)
        except User_Not_Found: return User_Not_Found
        except TypeError: return TypeError

    def check_permissions(self, user, permission):
        user_role_list = user.roles
        for role in user_role_list:
            if permission in self.role_store[role]:
                return True
        return False

    def checkout_item(self, item, user):
        # Validate customer type
        if not(isinstance(user, User)):
            print("Checkout user is not a user")
            raise Not_User
        
        # validate if user has permissions
        if not(self.check_permissions(user, "checkout_books")):
            print("Does not have permission to checkout books")
            raise PermissionError("Does not have permission to checkout books")
        
        # Validate book type
        if not(isinstance(item, Book)):
            print("Checkout item is not a book")
            raise Not_Book
        
        # create new transaction
        new_transaction = Transaction(user.id, item.id)
        self.transaction_store.add_transaction(new_transaction)
        receipt = f"{new_transaction.item_id} {new_transaction.customer_id} {new_transaction.checkout_date}"
        print(f"Your receipt is {receipt}")
        
        # remove the book from the item storage
        try:
            self.book_store.remove_book(item)
        except Book_Not_Found: return Book_Not_Found
        except Book_None_Available: return Book_None_Available
        
        # return receipt
        return receipt
        
    def return_book(self, receipt):
        # find the transaction from the storage
        try:
            transaction = self.transaction_store.find_transaction(receipt)
        except No_Transaction_Present: return No_Transaction_Present
        
        # change the return date
        transaction.return_date = datetime.datetime.utcnow()
        self.transaction_store.write_file()
        
        # find the isbn for the book from the transaction details
        book_id = transaction.item_id
        
        # find the book object from the storage using the isbn
        try:
            book = self.book_store.find_isbn(book_id)
        except Book_Not_Found: Book_Not_Found
        
        # change details in the storage to book returned
        try:
            self.book_store.return_book(book)
        except Book_Not_Found: return Book_Not_Found
        
        # return new receipt
        return f"{receipt} {transaction.return_date}"
    
    def create_patron(self, user, name, email, number):
        # Type check
        if not(isinstance(user, User)):
            print("User is not a user type")
            raise Not_User
        
        # permission check
        if not(self.check_permissions(user, "add_patrons")):
            print("Does not have permission to add patrons")
            raise PermissionError("Does not have permission to add patrons")
        
        # creating patron
        print("Creating new user")
        new_patron = User(name, email, number)
        
        # setting roles for patron
        print("Adding patron role")
        new_patron.add_role(Role("Patron", ["checkout_books", "return_books"]))
        print("Saving user")
        
        # saving user to store
        try:
            self.user_store.add_user(new_patron)
        except User_Already_Exists: return User_Already_Exists
        return new_patron.id
    
    def delete_patron(self, user, patron_id):
        # type validation
        if not(isinstance(patron_id, str)):
            print("enter the patron ID as a string")
            raise TypeError("Enter a string")
        if not(isinstance(user, User)):
            print("User is not a user type")
            raise Not_User
        
        # permission validation
        if not(self.check_permissions(user, "delete_patrons")):
            print("Does not have permission to delete patrons")
            raise PermissionError("Does not have permission to delete patrons")
        
        # finding user
        try: patron = self.user_store.find_user_id(patron_id)
        except User_Not_Found: return User_Not_Found
        
        # deleting user
        print("Deleting patron")
        self.user_store.remove_user(patron)
        return patron_id
    
    def create_librarian(self, user, name, email, number):
        # Type check
        if not(isinstance(user, User)):
            print("User is not a user type")
            raise Not_User
        
        # permission check
        if not(self.check_permissions(user, "add_librarians")):
            print("Does not have permission to add librarians")
            raise PermissionError("Does not have permission to add librarians")
        
        # creating librarian account
        print("Creating new user")
        new_librarian = User(name, email, number)
        print("Adding librarian role")
        
        # adding librarian role
        new_librarian.add_role(Role("Librarian", ["add_patrons", "add_librarians", "remove_patrons", "remove_librarians", "add_books", "remove_books"]))
        
        # saving user to store
        try:
            self.user_store.add_user(new_librarian)
        except User_Already_Exists: return User_Already_Exists
        return new_librarian.id
    
    def delete_librarian(self, user, librarian_id):
        # type validation
        if not(isinstance(librarian_id, str)):
            print("enter the librarian ID as a string")
            raise TypeError("Enter a string")
        if not(isinstance(user, User)):
            print("User is not a user type")
            raise Not_User
        
        # permission validation
        if not(self.check_permissions(user, "delete_librarians")):
            print("Does not have permission to delete librarians")
            raise PermissionError("Does not have permission to delete librarians")
        
        # finding user
        librarian = self.user_store.find_user_id(librarian_id)
        
        # deleting user
        print("Deleting patron")
        self.user_store.remove_user(librarian)
        return librarian_id
    
    def add_book(self, user, title, author, isbn, quantity = 1):
        # type validation
        if not(isinstance(user, User)):
            print("User is not a user type")
            raise Not_User
        
        # permission validation
        if not(self.check_permissions(user, "add_books")):
            print("Does not have permission to add books")
            raise PermissionError("Does not have permission to add books")
        
        # adding book to storage
        print("adding book")
        self.book_store.add_book(Book(title, author, isbn, quantity))
        return isbn
    
    def delete_book(self, user, book_isbn):
        # type validation
        if not(isinstance(user, User)):
            print("User is not a user type")
            raise Not_User
        if not(isinstance(book_isbn, str)):
            raise TypeError("Enter string for book ISBN")
        
        # permission validation
        if not(self.check_permissions(user, "delete_books")):
            print("Does not have permission to delete books")
            raise PermissionError("Does not have permission to delete books")
        
        # finding the book
        print("finding book")
        try: book = self.book_store.find_isbn(book_isbn)
        except Book_Not_Found: return Book_Not_Found
        
        # removing book from storage
        print("deleting book")
        try: self.book_store.delete_book(book)
        except Book_None_Available: Book_None_Available
        return book_isbn
    
    def book_details(self, book_isbn):
        # type validation
        if not(isinstance(book_isbn, str)):
            raise TypeError("Enter string for book ISBN")
        
        # finding the book
        print("finding book")
        book = self.book_store.find_isbn(book_isbn)
        
        # returning the book details
        return book.details()