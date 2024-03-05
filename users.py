from os import path
import json
import file_services as FS

class User:
    name : str
    email : str
    number : int
    id : int


class Patron(User):
    def __init__(self):
        super().__init__(self)
    
    

class Librarian(User):
    pass

class User_Storage:
    def add_patron(self, patron):
        pass
    
    def add_librarian(self, librarian):
        pass

class Patron_Encoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Patron):
            return {
                "name" : object.name,
                "email" : object.email,
                "number" : object.number,
                "id" : object.id
            }
        return super().default(object)

class Patron_Decoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(self, object_hook = self.to_object)
    
    def to_object(self, d):
        return Patron(d["name"], d["email"], d["number"], d["id"])
class Patron_File(User_Storage):
    def __init__(self, file_name = "Patron_List.json"):
        self.file_name = FS.CreateFilePath(file_name)
        self.books = self.load_file(self)
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, "r") as file_name:
                books_json = json.loads(file_name, '''cls = User_Decoder''')
        else: books_json = {}
        return books_json
    
    def write_file(self):
        with open(self.file_name) as file_name:
            json.dumps(self.books, file_name, sort_keys = True)