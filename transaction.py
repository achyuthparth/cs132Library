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
    
    def __init__(self, customer_id, item_id):
        self.customer_id = customer_id
        self.item_id = item_id
        self.checkout_date = datetime.datetime.utcnow()
        self.return_date = None
        delta = datetime.timedelta(weeks = 3)
        self.due_date = self.checkout_date + delta # 3 weeks time to return the book
        self.fine = 0 #self.calculate_fine() # calculates the fines based on how late the return is, $1 per week
    '''
    def calculate_fine(self):
        if self.return_date == None:
            time_difference = self.due_date - datetime.datetime.utcnow()
        else: time_difference = self.due_date - self.return_date
        return self.fine'''

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
            return { f"{object.item_id} {object.customer_id} {object.checkout_date}" :{
                "customer_id" : object.customer_id,
                "item_id" : object.item_id,
                "checkout_date" : str(object.checkout_date),
                "return_date" : str(object.return_date),
                "due_date" : str(object.due_date),
                "fine" : object.fine
            }}
        return super().default(object)

class Transaction_Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook = self.to_object)
        
    def to_object(self, d):
        if d == (None or {}):
            return {}
        for key, values in d.items():
            d[key] = Transaction(values["customer_id"], values["item_id"], datetime.datetime.fromisoformat(values["checkout_date"]), datetime.datetime.fromisoformat(values["return_date"]), datetime.datetime.fromisoformat(values["due_date"]), values["fine"])
        return d
class Transaction_File(Transaction_Store):
    def __init__(self, file_name = "Transaction_List.json"):
        self.file_name = FS.CreateFilePath(file_name)
        # error handling for load file
        self.transactions = self.load_file()
        if self.transactions is None:
            self.transactions = {}
    
    def load_file(self):
        file_exists = path.exists(self.file_name)
        if file_exists:
            with open(self.file_name, 'r') as file_name:
                transactions_json = json.load(file_name, cls = Transaction_Decoder)
        else:
            transactions_json = {}
        return transactions_json

    def write_file(self):
        with open(self.file_name, "w") as file_name:
            json.dump(self.transactions, file_name, cls = Transaction_Encoder, sort_keys = True)

    def add_transaction(self, transaction):
        receipt = f"{transaction.item_id} {transaction.customer_id} {transaction.checkout_date}"
        self.transactions[receipt] = transaction
        self.write_file()

    def find_transaction(self, receipt):
        return self.transactions.get(receipt)

    def save_to_store(self):
        self.write_file()