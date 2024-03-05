from os import path 
import json
import file_services as FS
class Book:
    title: str
    author : str
    isbn : str
    quantity : int
    available : int
    
    def details(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Quantity: {self.quantity}, Available: {self.available}"


class Book_Storage:
    def add_book(self, book):
        pass
    def delete_book(self, book):
        pass

class Book_Encoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Book):
            return {
                "title": object.title,
                "id": object.id,
                "author" : object.author,
                "isbn" : object.isbn,
                "quantity" : object.quantity,
                "available" : object.available
            }
        return super().default(object)

class Book_Decoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(self, object_hook = self.to_object)
    
    def to_object(self, d):
        return Book(d["title"], d["id"], d["author"], d["isbn"], d["quantity"], d["available"])
class Book_Not_Found(Exception): pass
class Book_None_Available(Exception): pass
class Book_File(Book_Storage):
    def __init__(self, file_name = "Book_List.json"):
        self.file_name = FS.CreateFilePath(file_name)
        self.books = self.load_file(self)
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, "r") as file_name:
                books_json = json.loads(file_name, '''cls = Book_Decoder''')
        else: books_json = {}
        return books_json
    
    def write_file(self):
        with open(self.file_name) as file_name:
            json.dumps(self.books, file_name, sort_keys = True)
    
    def add_book(self, book):
        book_list = self.books
        if isinstance(book, Book):
            book_key = book.isbn
            if book_key not in book_list:
                book_list[book_key] = book
            book_list[book_key].quantity += 1
            book_list[book_key].available += 1
        else: raise TypeError
    
    def delete_book(self, book):
        book_list = self.books
        if isinstance(book, Book):
            book_key = book.isbn
            if book_key not in book_list:
                raise Book_Not_Found
            if book_list[book_key].available < 1:
                raise Book_None_Available
            else: book_list[book_key].available -= 1; book_list[book_key].quantity -=1