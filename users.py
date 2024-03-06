from os import path
import json
import file_services as FS
class User:
    name : str
    email : str
    number : str
    id : int
    roles : list # save just the names, not the role objects themselves
    # implement add/remove role methods

class Patron(User): # use a single class, remove librarian and change patron to user
    def __init__(self, name, email, number, id):
        self.name = name
        self.email = email
        self.number = number
        self.id = id

class Librarian(User):
    def __init__(self):
        super().__init__(self)

class Patron_Storage:
    def add_patron(self, patron):
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
        json.JSONDecoder.__init__(self, object_hook = self.to_object)
    
    def to_object(self, d):
        if d == (None or {}):
            return {}
        return Patron(d["name"], d["email"], d["number"], d["id"])

class Not_A_Patron(TypeError): pass
class Patron_Not_Found(Exception): pass
class Patron_Already_Exists(Exception): pass
class Patron_File(Patron_Storage):
    def __init__(self, file_name = "Patron_List.json"):
        self.file_name = FS.create_file_path(file_name)
        self.patrons = self.load_file()
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, "r") as file_name:
                patrons_json = json.load(file_name, cls = Patron_Decoder)
        else: patrons_json = {}
        return patrons_json
    
    def write_file(self):
        with open(self.file_name, "w") as file_name:
            json.dump(self.patrons, file_name, cls = Patron_Encoder, sort_keys = True)
    
    def add_patron(self, patron):
        patron_list = self.patrons
        if isinstance(patron, Patron):
            if patron.id not in patron_list:
                patron_list[patron.id] = patron
            else: raise Patron_Already_Exists
        else: raise Not_A_Patron
        self.write_file()
        return patron.id in patron_list
    
    def remove_patron(self, patron):
        patron_list = self.patrons
        if isinstance(patron, Patron):
            if patron.id not in patron_list:
                raise Patron_Not_Found
            else:
                del patron_list[patron.id]
        else: raise Not_A_Patron
        self.write_file()
        return patron.id in patron_list