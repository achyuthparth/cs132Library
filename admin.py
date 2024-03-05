from users import User, Patron, Librarian
class Permission:
    name : str
    def __init__(self, name) -> None:
        self.name = name
    
    def __str__(self) -> str:
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

class Kiosk_User:
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

class User_Session:
    user : Kiosk_User
    active_roles : dict
    id : int
    def __init__(self, user):
        self.user = user
        self.active_roles = {}
        self.id = user.id

    def add_role(self, role):
        self.active_roles[role.name] = role

    def drop_role(self, role):
        del self.active_roles[role.name]
    
    def check_permission(self, permission):
# Iterate through active roles
        for role in self.active_roles.values():
# Check if required permission belongs to role
            if permission in role.permissions:
                return True
# Permission not found    
        return False
    
    