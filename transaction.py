from os import path
import json
import file_services as FS
import datetime
from collections import OrderedDict

class Transaction:
    customer_id : int
    item_id : str
    checkout_date : datetime.datetime
    return_date : datetime.datetime
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
    def default(self, o):
        return o.__dict__

class Transaction_Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.toObject)

class Transaction_File(Transaction_Store):
    def __init__(self, fileName = "Transaction_List.json"):
        self.FileName = FS.CreateFilePath(fileName)
        self.transactions = self.ReadFile()

    def ReadFile(self):
        fileExists = path.exists(self.FileName)
        if fileExists:
            with open(self.FileName, 'r') as self.FileName:
                transactions = json.load(self.FileName, cls = Transaction_Decoder)
        else:
            transactions = OrderedDict()
        return transactions

    def WriteFile(self):
        with open(self.FileName, "w") as outfile:
            json.dump(self.transactions, outfile, cls = Transaction_Encoder)
        return

    def add_transaction(self, transaction):
        transaction_dict = self.ReadFile()
        receipt = tuple(map(str, (transaction.item_id, transaction.customer_id, transaction.checkout_date)))
        transaction_dict[receipt] = transaction
        self.WriteFile()
    
    def find_transaction(self, receipt):
        for key, value in self.ReadFile().items():
            if key == receipt:
                return value
        return None
    
    def save_to_store(self):
        self.WriteFile()