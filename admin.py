from users import User, Patron, Librarian
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
    def __init__(self, name, permissions = {}):
        self.name = name
        self.permissions = permissions
        

    def add_permission(self, permission):
        if isinstance(permission, Permission):
            self.permissions.add(permission)
        else: raise Not_A_Permission
    
    def remove_permission(self, permission):
        if isinstance(permission, Permission):
            self.permissions.remove(permission)
        else: raise Not_A_Permission
    
    def __str__(self):
        return f"{self.name} : {self.permissions}"

class Permissions_Store: pass # for manipulating masterList of permissions
class Roles_Store: pass # manipulating masterList for roles and relationship to permissions

class Kiosk_User: # implement in the user class, not a new class
    id : int
    roles : set
    user : User
    def __init__(self, user, roles = {}):
        self.id = user.id
        self.roles = roles
        self.user = user

    def add_role(self, role):
        if isinstance(role, Role):
            self.roles.add(role)
        else: raise Not_A_Role

    def remove_role(self, role):
        if isinstance(role, Role):
            self.roles.remove(role)
        else: raise Not_A_Role

def has_permission(permission, user):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if permission in user.permissions:
                return func(*args, **kwargs)
            else:
                raise PermissionError("Access denied")
        return wrapper
    return decorator