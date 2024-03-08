import json
from os import path
#from users import User
class Permission: # implement store
    name : str
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class Not_A_Permission(TypeError): pass

class Permission_Store: # for manipulating master-list of permissions
    def add_permission(self, permission): pass
    def remove_permission(self, permission): pass
    def find_permission(self, permission): pass

class Permission_File(Permission_Store):
    def __init__(self, file_name = "Permission_List.json") -> None:
        self.file_name = file_name
        self.permissions = self.load_file() # dependency injection, loads only once
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, "r") as file_name:
                permissions_json = json.load(file_name)
        else: return set([])
        return set([Permission(perm) for perm in permissions_json])
    
    def write_file(self):
        permission_list = [permission.__str__() for permission in list(self.permissions)]
        with open(self.file_name, "w") as file_name:
            json.dump(permission_list, file_name)
    
    def add_permission(self, permission):
        if isinstance(permission, str):
            self.permissions.add(Permission(permission))
        else: raise TypeError("Enter a string")
    
    def find_permission(self, permission): # returns boolean whether the permission exists
        if isinstance(permission, str):
            return Permission(permission) in self.permissions
        else: raise TypeError("Enter a string")
    
    def remove_permission(self, permission):
        if isinstance(permission, str):
            self.permissions.remove(Permission(permission))
        else: raise TypeError("Enter a string")

class Not_A_Role(TypeError): pass

class Role:
    name : str
    permissions : set
    def __init__(self, name, permissions = None):
        self.name = name
        self.permissions = permissions
        if self.permissions is None: self.permissions = set([])

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

class Role_Encoder(json.JSONEncoder):
    def default(self, o):
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
        if self.load_file() is None:
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
    
    def write_file(self):
        role_list = [values for key, values in self.roles.items()]
        with open(self.file_name, "w") as file_name:
            json.dump(role_list, file_name, cls = Role_Encoder)
    
    def add_role(self, role):
        if isinstance(role, Role):
            name = role.name
            self.roles[name] = role
            self.write_file()
        else: raise Not_A_Role
        
    def find_role(self, name): # find the role and returns the permissions
        if isinstance(name, str):
            try:
                for key, values in self.roles.items():
                    if key == name:
                        return values
            except: Role_Not_Existent
        else: TypeError("Enter a string")
    
    def delete_role(self, role_name):
        if isinstance(role_name, str):
            try:
                del self.roles[role_name]
            except: Role_Not_Existent
        else: TypeError("Enter a string")
        self.write_file()

'''
def has_permission(permission, user):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if permission in user.permissions:
                return func(*args, **kwargs)
            else:
                raise PermissionError("Access denied")
        return wrapper
    return decorator
    '''