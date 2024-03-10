# Library will be the UI module

import tkinter
import kiosk

root = Tk()
root.title("Achyuthaa's Library")
class Library(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        container = Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        self.Frames = {}
        
        # frames needed are login frame, action choice frame, action frame
        for F in (Login_Frame, Patron_Frame, Librarian_Frame, Checkout_Frame, Return_Frame, Create_Patron_Frame, Delete_Patron_Frame, Add_Librarian_Frame, Delete_Librarian_Frame, Add_Book_Frame, Delete_Book_Frame, Book_Details_Frame):
            frame = F(container, self)
            frame.grid(row = 0, column = 0, sticky="nsew")
        
        # Activate frame
        self.show_frame(Login_Frame)
        goHomeButton = Button(self,
            text = "Go Home",
            command = lambda: self.show_frame(Login_Frame))
        goHomeButton.pack()
    
    def show_frame(self, frame_type_to_show):
        frame = self.Frames[frame_type_to_show]
        frame.Reset()
        frame.tkraise()

class Login_Frame(tkinter.Frame):
    def __init__(self, parent, application):
        self.Application = application
        tkinter.Frame.__init__(self, parent)
        self.login_frame = tkinter.LabelFrame(self, text = "Welcome to the Library")
        
        self.find_book_details = tkinter.Button(root, row = 5, padx = 3, pady = 3, text = "Find book details using ISBN", command = lambda : Library.show_frame(Book_Details_Frame))
        
        self.variable_login = tkinter.StringVar()
        self.login_input = tkinter.Entry(root, width = 50, borderwidth = 5)
        
        self.login_input.grid(row = 3, column = 4, columnspan = 3, padx = 10, pady = 10)
        self.login_input.insert("Enter user ID")
        self.user_id = self.login_input.get()
        
        self.login_button = tkinter.Button(root, text = "Login", command = self.login, padx = 3, pady = 3, row = 4, column = 4)
        self.login_input = tkinter.Entry(root, width = 50, borderwidth = 5)
    
    def login():
        tkinter.messagebox.showerror()
    
    def open_find_book():
        tkinter.messagebox.showerror()

    
    
    find_book_details = tkinter.Button(root, text = "Find book details using ISBN", command = open_find_book)
    


class Patron_Frame(tkinter.Frame): pass
class Librarian_Frame(tkinter.Frame): pass
class Checkout_Frame(tkinter.Frame): pass
class Return_Frame(tkinter.Frame): pass
class Create_Patron_Frame(tkinter.Frame): pass
class Delete_Patron_Frame(tkinter.Frame): pass
class Add_Librarian_Frame(tkinter.Frame): pass
class Delete_Librarian_Frame(tkinter.Frame): pass
class Add_Book_Frame(tkinter.Frame): pass
class Delete_Book_Frame(tkinter.Frame): pass
class Book_Details_Frame(tkinter.Frame): pass

root.mainloop()