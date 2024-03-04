class User:
    name : str
    email : str
    number : int
    id : int


class Patron(User):
    __password : str

class Librarian(User):
    __password : str
    
    @classmethod
    def create_patron(cls):
        return
    
    @classmethod
    def create_librarian(cls):
        return