from os import path
import json
import file_services as FS
from admin import Role, Not_A_Role

class User:
    name : str
    email : str
    number : str
    id : int
    roles : set # save just the names, not the role objects themselves
# using set as appending role to a list would create 2 instances
class User(User):
    def __init__(self, name, email, number, id, roles = set({})):
        self.name = name
        self.email = email
        self.number = number
        self.id = id
        self.roles = roles
    
    def add_role(self, role):
        if isinstance(role, str):
            self.roles.add(role)
        else: raise TypeError("Enter a string")

    def remove_role(self, role):
        if isinstance(role, str):
            self.roles.remove(role)
        else: raise TypeError("Enter a string")
        
class User_Storage:
    def add_user(self, user): pass
    def remove_user(self, user): pass

class User_Encoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, User):
            return {
                "name" : object.name,
                "email" : object.email,
                "number" : object.number,
                "id" : object.id,
                "roles" : list(object.roles) # converting set into list to save in json
            }
        return super().default(object)

class User_Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook = self.to_object)
    
    def to_object(self, d): # turn this into a list 
        if d == (None or {}):
            return []
        return User(d["name"], d["email"], d["number"], d["id"], set(d["roles"])) # converting list back into set

class Not_A_User(TypeError): pass
class User_Not_Found(Exception): pass
class User_Already_Exists(Exception): pass

class User_File(User_Storage):
    def __init__(self, file_name = "User_List.json"):
        self.file_name = FS.create_file_path(file_name)
        self.users = self.load_file()
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, "r") as file_name:
                user_json = json.load(file_name, cls = User_Decoder)
        else: return {}
        user_dict = {}
        for person in user_json:
            user_dict[person.id] = person
        return user_dict
    
    def write_file(self):
        user_list = []
        for key, values in self.users.items():
            user_list.append(values)
        with open(self.file_name, "w") as file_name:
            json.dump(user_list, file_name, cls = User_Encoder, sort_keys = True)
    
    def add_user(self, user):
        user_list = self.users
        if isinstance(user, User):
            if user.id not in user_list:
                user_list[user.id] = user
            else: raise User_Already_Exists
        else: raise Not_A_User
        self.write_file()
        return user.id in user_list
    
    def remove_user(self, user):
        user_list = self.users
        if isinstance(user, User):
            if user.id not in user_list:
                raise User_Not_Found
            else:
                del user_list[user.id]
        else: raise Not_A_User
        self.write_file()
        return user.id in user_list