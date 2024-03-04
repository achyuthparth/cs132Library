class Book:
    title: str
    id: int
    author : str
    isbn : str
    quantity : int
    available : int
    
    def details(self):
        return f"Title: {self.title}, ID: {self.id}, Author: {self.author}, ISBN: {self.isbn}, Quantity: {self.quantity}, Available: {self.available}"