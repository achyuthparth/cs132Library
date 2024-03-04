class Item: # abstract class
    title: str
    details : str
    id: int
    def details(self):
        return self.details

class Book(Item):
    author : str
    isbn : str

class DVD(Item):
    director : str
    isbn : str

class Misc(Item):
    pass