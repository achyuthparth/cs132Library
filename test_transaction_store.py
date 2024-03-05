import unittest
import datetime
from transaction import Transaction_File, Transaction

transaction_1 = Transaction(2,"34")
transaction_2 = Transaction(1, "42")
transaction_3 = Transaction(3, "56")
class Test(unittest.TestCase):
    def setup1(self):
        store_1 = Transaction_File()
        store_1.add_transaction(transaction_1)
        for key, values in store_1.transactions.items():
            print(key)
            print(f"\n{values.customer_id} {values.item_id} {values.checkout_date} {values.return_date} {values.due_date} {values.fine}")
    
    def setup1(self):
        store_2 = Transaction_File()
        store_2.add_transaction(transaction_2)
        for key, values in store_2.transactions.items():
            print(key)
            print(f"\n{values.customer_id} {values.item_id} {values.checkout_date} {values.return_date} {values.due_date} {values.fine}")

if __name__ == '__main__':
    unittest.main()