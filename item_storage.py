from os import path 
import json
import file_services as FS
class Book:
    title: str
    author : str
    isbn : str
    quantity : int
    available : int
    def __init__(self, title, author, isbn, quantity = 1):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
    
    def details(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Quantity: {self.quantity}, Available: {self.available}"

class Book_Storage: # abstract storage class, using json now but can use db later
    
    def add_book(self, book): # for adding a new book to the library
        pass
    
    def delete_book(self, book): # for totally deleting book from library
        pass
    
    def remove_book(self, book): # for checkout method
        pass
    
    def return_book(self, book): # for returning a book after checkout
        pass

class Book_Encoder(json.JSONEncoder): # json encoder/decoder for custom book object
    def default(self, object):
        if isinstance(object, Book):
            return {
                "title": object.title,
                "author" : object.author,
                "isbn" : object.isbn,
                "quantity" : object.quantity,
                "available" : object.available
            }
        return super().default(object)

class Book_Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook = self.to_object)
    
    def to_object(self, d):
        if d == ([] or None):
            return []
        return Book(d["title"], d["id"], d["author"], d["isbn"], d["quantity"], d["available"])
class Book_Not_Found(Exception): pass
class Book_None_Available(Exception): pass
class Not_A_Book(TypeError): pass
class Book_File(Book_Storage): # concrete storage class which utilizes json
    def __init__(self, file_name = "Book_List.json"):
        self.file_name = FS.create_file_path(file_name)
        self.books = self.load_file()
        if self.books is None:
            self.books = {}
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, "r") as file_name:
                books_json = json.loads(file_name, cls = Book_Decoder)
        else: return {}
        return_dict = {}
        for item in books_json:
            return_dict[f"{item.isbn}"] = item
        return return_dict
    
    def write_file(self):
        book_list = [values for key, values in self.books.items()]
        with open(self.file_name, "w") as file_name:
            json.dump(book_list, file_name, cls = Book_Encoder)
    
    def find_book(self, book):
        if not(isinstance(book, Book)):
            raise Not_A_Book
        else: 
            try:
                return self.books(book.isbn)
            except: Book_Not_Found
    
    def find_isbn(self, isbn):
        if not(isinstance(isbn, str)):
            raise TypeError("Enter a string")
        else: 
            try:
                return self.books(isbn)
            except: Book_Not_Found
    
    def add_book(self, book):
        if isinstance(book, Book):
            if book.isbn not in self.books:
                self.books[book.isbn] = book
                self.books[book.isbn].available = book.quantity
            else:
                self.books[book.isbn].quantity += book.quantity
                self.books[book.isbn].available += book.quantity
        else: raise Not_A_Book
        self.write_file()
    
    def delete_book(self, book):
        if isinstance(book, Book):
            if book.isbn not in self.books:
                raise Book_Not_Found
            if self.books[book.isbn].available < 1: # in case book exists but is checked out
                raise Book_None_Available
            else:
                self.books[book.isbn].available -= 1
                self.books[book.isbn].quantity -=1
        else: raise Not_A_Book
        self.write_file()
    
    def remove_book(self, book):
        if isinstance(book, Book):
            if book.isbn not in self.books:
                raise Book_Not_Found
            if self.books[book.isbn].available < 1:
                raise Book_None_Available
            else:
                self.books[book.isbn].available -= 1
        else: raise Not_A_Book
        self.write_file()
    
    def return_book(self, book):
        if isinstance(book, Book):
            if book.isbn not in self.books:
                raise Book_Not_Found
            else:
                self.books[book.isbn].available += 1
        else: raise Not_A_Book
        self.write_file()