from os import path
import json
import file_services as FS
import datetime

class Transaction(dict):
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
                "checkout_date" : object.checkout_date,
                "return_date" : object.return_date,
                "due_date" : object.due_date,
                "fine" : object.fine
            }
        return super().default(object)

class Transaction_Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook = self.to_object)
        
    def to_object(self, d):
        return Transaction(d["customer_id"], d["item_id"], d["checkout_date"], d["return_date"], d["due_date"], d["fine"])

class Transaction_File(Transaction_Store):
    def __init__(self, file_name = "Transaction_List.json"):
        self.file_name = FS.CreateFilePath(file_name)
        self.transactions = self.load_file()
    
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
        receipt = "".join(tuple(map(str, (transaction.item_id, transaction.customer_id, transaction.checkout_date))))
        self.transactions[receipt] = transaction
        self.write_file()

    def find_transaction(self, receipt):
        return self.transactions.get(receipt)

    def save_to_store(self):
        self.write_file()