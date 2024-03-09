# Library will be the UI module

from tkinter import *
import kiosk

root = Tk()
root.title("Achyuthaa's Library")
class Library(Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        container = Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        self.Frames = {}
# frames needed are login frame, action choice frame, action frame
        for F in (Login_Frame, Patron_Frame, Librarian_Frame, Checkout_Frame, Return_Frame, Create_Patron_Frame, Delete_Patron_Frame, Add_Librarian_Frame, Delete_Librarian_Frame, Add_Book_Frame, Delete_Book_Frame, Book_Details_Frame):
            frame = F(container, self)
            frame.grid(row=0, colomn=0)
        self.show_frame(Login_Frame)
        goHomeButton = Button(self,
            text = "Go Home",
            command = lambda: self.show_frame(Login_Frame))
        goHomeButton.pack()
    
    def show_frame(self, frame_type_to_show):
        frame = self.Frames[frame_type_to_show]
        frame.Reset()
        frame.tkraise()

class Login_Frame(Frame):
    def __init__(self, parent, application):
        self.Application = application
        Frame.__init__(self, parent)
        startFrame = LabelFrame(self, text = "Welcome to the Library")
    variable_login = StringVar()
    login_input = Entry(root, width = 50, borderwidth = 5)
    login_input.grid(row = 3, column = 4, columnspan = 3, padx = 10, pady = 10)
    login_input.insert("Enter user ID")
    user_id = login_input.get()
    login_button = Button(root, text = "Login")
    
    variable_book_details = StringVar()
    find_book_details = Button(root, text = "Find book details using ISBN", variable = variable_book_details)
    


class Patron_Frame(Frame): pass
class Librarian_Frame(Frame): pass
class Checkout_Frame(Frame): pass
class Return_Frame(Frame): pass
class Create_Patron_Frame(Frame): pass
class Delete_Patron_Frame(Frame): pass
class Add_Librarian_Frame(Frame): pass
class Delete_Librarian_Frame(Frame): pass
class Add_Book_Frame(Frame): pass
class Delete_Book_Frame(Frame): pass
class Book_Details_Frame(Frame): pass

root.mainloop()