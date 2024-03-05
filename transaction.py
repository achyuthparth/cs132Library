from os import path
import json
import file_services as FS
import datetime

class Transaction:
    customer_id : int
    item_id : str
    checkout_date : datetime.datetime
    return_date : datetime.datetime
    due_date : datetime.datetime
    fine : float
    
    def __init__(self, customer_id, item_id, checkout_date = None, return_date = None, due_date = None, fine = None):
        self.customer_id = customer_id
        self.item_id = item_id
        if checkout_date == None: self.checkout_date = datetime.datetime.utcnow() 
        else: self.checkout_date = checkout_date
        if return_date == None: self.return_date = self.checkout_date
        else: self.return_date = return_date
        delta = datetime.timedelta(weeks = 3)
        if due_date == None: self.due_date = self.checkout_date + delta # 3 weeks time to return the book
        else: self.due_date = due_date
        if fine == None: self.fine = 0 #self.calculate_fine() # calculates the fines based on how late the return is, $1 per week
        else: self.fine = self.calculate_fine()
    
    def calculate_fine(self):
        if self.return_date == self.checkout_date:
            time_difference = (self.due_date - datetime.datetime.utcnow()).days
        else: time_difference = (self.due_date - self.return_date).days
        if time_difference < 0:
            weeks_passed = abs(time_difference)//7
            self.fine += weeks_passed
            return self.fine
        return self.fine

class Transaction_Store:
    
    def add_transaction(self, transaction):
        pass

    def find_transaction(self, receipt):
        pass
    
    def save_to_store(self):
        pass

class Transaction_Encoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Transaction):
            return {
                "customer_id" : object.customer_id,
                "item_id" : object.item_id,
                "checkout_date" : datetime.datetime.strftime(object.checkout_date, "%Y-%m-%d %H:%M:%S"),
                "return_date" : datetime.datetime.strftime(object.return_date, "%Y-%m-%d %H:%M:%S"),
                "due_date" : datetime.datetime.strftime(object.due_date, "%Y-%m-%d %H:%M:%S"),
                "fine" : object.fine
            }
        return super().default(object)

class Transaction_Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook = self.to_object)
    
    def to_object(self, d):
        if d == (None or {}):
            return {}
        return Transaction(d["customer_id"], d["item_id"], datetime.datetime.strptime(d["checkout_date"], "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime(d["return_date"], "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime(d["due_date"], "%Y-%m-%d %H:%M:%S"), d["fine"])
class No_Transaction_Present(Exception): pass
class Transaction_File(Transaction_Store):
    def __init__(self, file_name = "Transaction_List.json"):
        self.file_name = FS.create_file_path(file_name)
        # error handling for load file
        self.transactions = self.load_file()
        if self.transactions is None:
            self.transactions = {}
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, 'r') as file_name:
                transactions_json = json.load(file_name, cls = Transaction_Decoder)
        else: transactions_json = {}
        return transactions_json

    def write_file(self):
        with open(self.file_name, "w") as file_name:
            json.dump(self.transactions, file_name, cls = Transaction_Encoder)

    def add_transaction(self, transaction):
        receipt = f"{transaction.customer_id} {transaction.item_id} {transaction.checkout_date}"
        self.transactions[receipt] = transaction
        self.write_file()

    def find_transaction(self, receipt):
        try:
            for key, values in self.transactions.items():
                if key == receipt:
                    return values
        except: No_Transaction_Present
    
    def save_to_store(self):
        self.write_file()