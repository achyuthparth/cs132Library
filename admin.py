import json
from os import path
from users import User2, User2, Librarian
class Permission: # implement store
    name : str
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class Not_A_Permission(TypeError): pass
class Not_A_Role(TypeError): pass

class Role:
    name : str
    permissions : set
    def __init__(self, name, permissions = []):
        self.name = name
        self.permissions = permissions
        

    def add_permission(self, permission):
        if isinstance(permission, str):
            self.permissions.add(permission)
        else: raise TypeError("Enter a string")
    
    def remove_permission(self, permission):
        if isinstance(permission, Permission):
            self.permissions.remove(permission)
        else: raise TypeError("Enter a string")
    
    def find_permission(self, permission_name: str):
        if isinstance(permission_name, str):
            return permission_name in self.permissions
        else: raise TypeError("Enter a string")
    
    def __str__(self):
        return f"{self.name} : {self.permissions}"

class Permissions_Store: pass # for manipulating master-list of permissions

class Role_Encoder(json.JSONEncoder):
    def default(self, o: json.Any) -> json.Any:
        if isinstance(o, Role):
            return {
                "name" : o.name,
                "permissions" : o.permissions
            }
        return super().default(o)
class Role_Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook = self.to_object)
    
    def to_object(self, d):
        if d == (None or []):
            return []
        return Role(d["name"], d["permissions"])
class Roles_Store: # manipulating master-list for roles and relationship to permissions
    def add_role(self, role): pass
    def delete_role(self, role): pass
    def find_role(self, role): pass

class Role_Not_Existent(Exception): pass

class Role_File(Roles_Store):
    def __init__(self, file_name = "Role_List.json") -> None:
        self.file_name = file_name
        self.roles = self.load_file()
        if self.load_file is None:
            self.roles = {}
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, "r") as file_name:
                roles_json = json.load(file_name, cls = Role_Decoder)
        else: return {}
        roles_dict = {}
        for item in roles_json:
            roles_dict[f"{item.name}"] = item
        return roles_dict
    def write_file(self): # convert self.transaction into a list
        transaction_list = []
        for key, values in self.roles.items():
            transaction_list.append(values)
        with open(self.file_name, "w") as file_name:
            json.dump(transaction_list, file_name, cls = Role_Encoder)
    
    def add_role(self, role):
        if isinstance(role, Role):
            name = role.name
            self.roles[name] = role
            self.write_file()
        else: raise Not_A_Role
        
    def find_role(self, name):
        try:
            for key, values in self.roles.items():
                if key == name:
                    return values
        except: Role_Not_Existent
    
    def delete_role(self, role):
        name = role.name
        del self.roles[name]
        self.write_file

def has_permission(permission, user):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if permission in user.permissions:
                return func(*args, **kwargs)
            else:
                raise PermissionError("Access denied")
        return wrapper
    return decorator