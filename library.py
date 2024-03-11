# Library will be the UI module

import tkinter
from tkinter import *
from kiosk import Kiosk, User_Not_Found, Not_User, Not_Book, Book_Not_Found, Book_None_Available, No_Transaction_Present, User_Already_Exists
from users import User_File
from transaction import Transaction_File
from item_storage import Book_File
from roles import Role_File
from tkinter import messagebox

# initializing file services
user_store = User_File()
transaction_store = Transaction_File()
book_store = Book_File()
role_store = Role_File()
my_kiosk = Kiosk(transaction_store, role_store, book_store, user_store)
logged_user = None

class Library(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        container = tkinter.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        self.frames = {}
        
        # frames needed are login frame, action choice frame, action frame
        for F in (Login_Frame, Patron_Frame, Librarian_Frame, Checkout_Frame, Return_Frame, Create_Patron_Frame, Delete_Patron_Frame, Add_Librarian_Frame, Delete_Librarian_Frame, Add_Book_Frame, Delete_Book_Frame, Book_Details_Frame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")
        
        # Activate frame
        self.show_frame(Login_Frame)
        
        # Go home button
        goHomeButton = tkinter.Button(self,
            text = "Go Home",
            command = lambda: self.show_frame(Login_Frame))
        goHomeButton.pack()
    
    # function to activate different frame
    def show_frame(self, frame_type_to_show):
        if frame_type_to_show == Login_Frame:
            global logged_user
            logged_user = None
        
        # put new frame on old
        frame = self.frames[frame_type_to_show]
        #tkinter.Frame.destroy(frame)
        tkinter.Frame.tkraise(frame)

class Login_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        # setting up connection to main UI unit
        self.Library = library
        tkinter.Frame.__init__(self, parent)
        self.login_frame = tkinter.LabelFrame(self, text = "Welcome to the Library")
        
        # defining button to get book details
        self.book_details_button = tkinter.Button(self.login_frame, padx = 3, pady = 3, text = "Find book details", command = lambda : Library.show_frame(self.Library, Book_Details_Frame))
        
        # creating input box to enter user login information
        self.login_input = tkinter.Entry(self.login_frame, width = 50, borderwidth = 5)
        self.login_input.insert(0, "Enter Uer ID")
        
        # creating button to activate the login
        self.login_button = tkinter.Button(self.login_frame, text = "Login", command = self.login, padx = 3, pady = 3)
        
        # packing to frame
        self.login_frame.pack()
        self.book_details_button.pack()
        self.login_input.pack()
        self.login_button.pack()
    
    def login(self):
        try:
            global logged_user
            logged_user = my_kiosk.login(self.login_input.get())
            if "Patron" in logged_user.roles: Library.show_frame(self.Library, Patron_Frame)
            elif "Librarian" in logged_user.roles: self.Library.show_frame(Librarian_Frame)
            else: messagebox.showerror("", "User role does not exist")
        except TypeError: messagebox.showerror("", "Type error")
        except User_Not_Found: messagebox.showerror("", "User not found")
        except: messagebox.showerror("", "Login Failed")

class Patron_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        # setting up connection to main UI unit
        self.Library = library
        tkinter.Frame.__init__(self, parent)
        self.patron_frame = tkinter.LabelFrame(self, text = "Patron Menu")
        
        # setting up buttons for action
        self.checkout_button = tkinter.Button(self.patron_frame, padx = 3, pady = 3, text = "Checkout Book", command = lambda : self.Library.show_frame(Checkout_Frame))
        self.return_button = tkinter.Button(self.patron_frame, text = "Return Book", command = lambda : self.Library.show_frame(Return_Frame))
        
        # packing
        self.patron_frame.pack()
        self.checkout_button.pack()
        self.return_button.pack()

class Librarian_Frame(tkinter.Frame): # add generating reports
    def __init__(self, parent, library):
        # setting up connection to main UI unit
        self.Library = library
        tkinter.Frame.__init__(self, parent)
        self.librarian_frame = tkinter.LabelFrame(self, text = "Librarian Menu")
        
        # setting up buttons for action
        self.create_patron_button = tkinter.Button(self.librarian_frame, padx = 3, pady = 3, text = "Create Patron", command = lambda : self.Library.show_frame(Create_Patron_Frame))
        self.delete_patron_button = tkinter.Button(self.librarian_frame, text = "Delete Patron", command = lambda : self.Library.show_frame(Delete_Patron_Frame))
        self.create_librarian_button = tkinter.Button(self.librarian_frame, padx = 3, pady = 3, text = "Create Librarian", command = lambda : self.Library.show_frame(Add_Librarian_Frame))
        self.delete_librarian_button = tkinter.Button(self.librarian_frame, text = "Delete Librarian", command = lambda : self.Library.show_frame(Delete_Librarian_Frame))
        self.add_book_button = tkinter.Button(self.librarian_frame, padx = 3, pady = 3, text = "Add New Book to Library", command = lambda : self.Library.show_frame(Add_Book_Frame))
        self.delete_book_button = tkinter.Button(self.librarian_frame, text = "Remove Book from Library", command = lambda : self.Library.show_frame(Delete_Book_Frame))
        
        #packing
        self.librarian_frame.pack()
        self.create_patron_button.pack()
        self.delete_patron_button.pack()
        self.create_librarian_button.pack()
        self.delete_librarian_button.pack()
        self.add_book_button.pack()
        self.delete_book_button.pack()

class Checkout_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.checkout_frame = tkinter.LabelFrame(self, text = "Checkout a Book")
        
        self.isbn_input = tkinter.Entry(self.checkout_frame, width = 50, borderwidth = 5)
        self.isbn_input.insert(0, "Enter Book ISBN")
        
        self.details_button = tkinter.Button(self.checkout_frame, text = "Checkout", command = self.checkout_book, padx = 3, pady = 3)
        
        self.checkout_frame.pack()
        self.isbn_input.pack()
        self.details_button.pack()
    
    def checkout_book(self):
        try: 
            global logged_user
            messagebox.showinfo(my_kiosk.checkout_item(logged_user, self.isbn_input.get())) # share receipt
        except PermissionError: messagebox.showerror("Permission not granted") # permission not granted
        except Book_Not_Found: messagebox.showerror("Book not found")
        except Book_None_Available: messagebox.showerror("Book not available")


class Return_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.return_frame = tkinter.LabelFrame(self, text = "Return a Book")
        
        self.receipt_input = tkinter.Entry(self.return_frame, width = 50, borderwidth = 5)
        self.receipt_input.insert(0, "Enter Transaction Receipt")
        
        
        self.details_button = tkinter.Button(self.return_frame, text = "Return", command = self.return_book, padx = 3, pady = 3)
        
        self.return_frame.pack()
        self.receipt_input.pack()
        self.details_button.pack()
    
    def return_book(self):
        try: messagebox.showinfo(my_kiosk.return_book(self.receipt_input.get())) # share new receipt
        except PermissionError: messagebox.showerror("","Permission not granted") # permission not granted
        except Book_Not_Found: messagebox.showerror("","Book not found")
        except No_Transaction_Present: messagebox.showerror("","Transaction does not exist")

class Create_Patron_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.create_patron_frame = tkinter.LabelFrame(self, text = "Create a Patron Account")
        
        # name for new account
        self.name_input = tkinter.Entry(self.create_patron_frame, width = 50, borderwidth = 5)
        self.name_input.insert(0, "Enter Name")
        
        # email for new account
        self.email_input = tkinter.Entry(self.create_patron_frame, width = 50, borderwidth = 5)
        self.email_input.insert(0, "Enter Email Address")
        
        # number for new account
        self.number_input = tkinter.Entry(self.create_patron_frame, width = 50, borderwidth = 5)
        self.number_input.insert(0, "Enter Phone Number")
        
        # activation button
        self.create_patron_button = tkinter.Button(self.create_patron_frame, text = "Create", command = self.create_patron, padx = 3, pady = 3)
        
        # packing
        self.create_patron_frame.pack()
        self.name_input.pack()
        self.email_input.pack()
        self.number_input.pack()
        self.create_patron_button.pack()
        
    def create_patron(self):
        try: # returns new patron's ID
            messagebox.showinfo("", f"New ID : {my_kiosk.create_patron(logged_user, self.name_input.get(), self.email_input.get(), self.number_input.get())}")
        except PermissionError: messagebox.showerror("Permission not granted")
        except User_Already_Exists: messagebox.showerror("User already exists")

class Delete_Patron_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.delete_patron_frame = tkinter.LabelFrame(self, text = "Delete Patron Account")
        
        self.patron_id_input = tkinter.Entry(self.delete_patron_frame, width = 50, borderwidth = 5)
        self.patron_id_input.insert(0, "Enter Patron Account ID")
        
        self.activate_delete = tkinter.Button(self.delete_patron_frame, text = "Delete", command = self.delete_patron, padx = 3, pady = 3)
        
        self.delete_patron_frame.pack()
        self.patron_id_input.pack()
        self.activate_delete.pack()
    
    def delete_patron(self):
        try:
            if not(my_kiosk.delete_patron(self.patron_id_input.get())):
                messagebox.showinfo(f"Successfully deleted {self.patron_id_input.get()}") # removal was successful
        except PermissionError: messagebox.showerror("Permission Error", "Does not have permission to delete patron accounts")
        except User_Not_Found: messagebox.showerror("User not found")
        except: messagebox.showerror("", f"Deletion Failed") # removal was unsuccessful

class Add_Librarian_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.create_librarian_frame = tkinter.LabelFrame(self, text = "Create a Librarian Account")
        
        # name for new account
        self.name_input = tkinter.Entry(self.create_librarian_frame, width = 50, borderwidth = 5)
        self.name_input.insert(0, "Enter Name")
        
        # email for new account
        self.email_input = tkinter.Entry(self.create_librarian_frame, width = 50, borderwidth = 5)
        self.email_input.insert(0, "Enter Email Address")
        
        # number for new account
        self.number_input = tkinter.Entry(self.create_librarian_frame, width = 50, borderwidth = 5)
        self.number_input.insert(0, "Enter Phone Number")
        
        # activation button
        self.create_librarian_button = tkinter.Button(self.create_librarian_frame, text = "Create", command = self.create_librarian, padx = 3, pady = 3)
        
        # packing
        self.create_librarian_frame.pack()
        self.name_input.pack()
        self.email_input.pack()
        self.number_input.pack()
        self.create_librarian_button.pack()
        
    def create_librarian(self):
        try: # returns new patron's ID
            messagebox.showinfo("", f"New User ID: {my_kiosk.create_librarian(logged_user, self.name_input.get(), self.email_input.get(), self.number_input.get())}")
        except PermissionError: messagebox.showerror("","Permission not granted")
        except User_Already_Exists: messagebox.showerror("","User already exists")

class Delete_Librarian_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.delete_librarian_frame = tkinter.LabelFrame(self, text = "Delete Librarian Account")
        
        self.librarian_id_input = tkinter.Entry(self.delete_librarian_frame, width = 50, borderwidth = 5)
        self.librarian_id_input.insert(0, "Enter Librarian Account ID")
        
        self.activate_delete = tkinter.Button(self.delete_librarian_frame, text = "Delete", command = self.delete_librarian, padx = 3, pady = 3)
        
        self.delete_librarian_frame.pack()
        self.librarian_id_input.pack()
        self.activate_delete.pack()
    
    def delete_librarian(self):
        try:
            my_kiosk.delete_librarian(self.librarian_id_input.get())
            messagebox.showinfo("Success",f"{self.librarian_id_input.get()} removed successfully") # removal was successful
        except PermissionError: messagebox.showerror("Permission Error", "Does not have permission to delete librarians")
        except User_Not_Found: messagebox.showerror("User not found", "User does not exist")
        except: messagebox.showerror("Removal failed", "Removal process has failed") # removal was unsuccessful


class Add_Book_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.add_book_frame = tkinter.LabelFrame(self, text = "Add New Book to Library")
        
        # title
        self.title_input = tkinter.Entry(self.add_book_frame, width = 50, borderwidth = 5)
        self.title_input.insert(0, "Enter Title")
        
        # author
        self.author_input = tkinter.Entry(self.add_book_frame, width = 50, borderwidth = 5)
        self.author_input.insert(0, "Enter Author")
        
        # isbn
        self.isbn_input = tkinter.Entry(self.add_book_frame, width = 50, borderwidth = 5)
        self.isbn_input.insert(0, "Enter ISBN")
        
        # number of books
        self.number_input = tkinter.Entry(self.add_book_frame, width = 50, borderwidth = 5)
        self.number_input.insert(0, "Enter Quantity")
        
        # activation button
        self.add_book_button = tkinter.Button(self.add_book_frame, text = "Add", command = self.add_book, padx = 3, pady = 3)
        
        # packing
        self.add_book_frame.pack()
        self.title_input.pack()
        self.author_input.pack()
        self.number_input.pack()
        self.add_book_button.pack()
        
    def add_book(self):
        try: # returns new patron's ID
            (my_kiosk.add_book(logged_user, self.title_input.get(), self.author_input.get(), self.isbn_input.get(), self.number_input.get()))
            messagebox.showinfo("Success", "Book added successfully")
        except PermissionError: messagebox.showerror("Permission Error","Permission not granted")

class Delete_Book_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.delete_book_frame = tkinter.LabelFrame(self, text = "Remove Book from Library")
        
        self.book_id_input = tkinter.Entry(self.delete_book_frame, width = 50, borderwidth = 5)
        self.book_id_input.insert(0, "Enter Book ISBN")
        
        self.activate_delete = tkinter.Button(self.delete_book_frame, text = "Delete", command = self.delete_book, padx = 3, pady = 3)
        
        self.delete_book_frame.pack()
        self.book_id_input.pack()
        self.activate_delete.pack()
    
    def delete_book(self):
        try: messagebox.showinfo(my_kiosk.delete_book(self.book_id_input.get()))
        except Book_Not_Found: messagebox.showerror("Book not found")
        except Book_None_Available: messagebox.showerror("Book not available")

class Book_Details_Frame(tkinter.Frame):
    def __init__(self, parent, library):
        tkinter.Frame.__init__(self, parent)
        self.Library = library
        
        self.book_details_frame = tkinter.LabelFrame(self, text = "Explore Book Details")
        
        # creating input box to get details via isbn
        
        self.isbn_input = tkinter.Entry(self.book_details_frame, width = 50, borderwidth = 5, text = "Enter Book ISBN")
        
        
        # button to find the book
        self.details_button = tkinter.Button(self.book_details_frame, text = "Return Details", command = self.book_details, padx = 3, pady = 3)
        
        # list all books button
        self.list_all = tkinter.Button(self.book_details_frame, text = "List Full Catalog", command = self.list_books, padx = 3, pady = 3)
        
        # pack to frame
        self.book_details_frame.pack()
        self.isbn_input.pack()
        self.details_button.pack()
        self.list_all.pack()
    
    def book_details(self): 
        global my_kiosk
        try: messagebox.showinfo("Details", f"{my_kiosk.book_details(self.isbn_input.get())}")
        except Book_Not_Found: messagebox.showerror("Details", "Book not found")
    
    def list_books(self):
        str_lst = ""
        for key, values in book_store.books.items():
            str_lst += (f"\nISBN : {key} \nTitle: {values.title} \nAuthor: {values.author} \nCopies Available: {values.available}\n")
        messagebox.showinfo(f"Entire catalog", f"{str_lst}")


root = Library()
root.mainloop()