import unittest
import datetime
from transaction import Transaction_File, Transaction

transaction_1 = Transaction(2,"34")
transaction_2 = Transaction(1, "42")
transaction_3 = Transaction(3, "56")
class TestTransaction(unittest.TestCase):
    store = Transaction_File()
    def test_setup1(self):
        store_1 = TestTransaction.store
        store_1.add_transaction(transaction_1)
        for key, values in store_1.transactions.items():
            print(key)
            print(f"\nCustomer {values.customer_id} \nItem {values.item_id} \nCheckout Date {values.checkout_date} \nReturn Date {values.return_date} \nDue Date {values.due_date} \nFines {values.fine}\n")
    
    def test_setup2(self):
        store_2 = TestTransaction.store
        store_2.add_transaction(transaction_2)
        for key, values in store_2.transactions.items():
            print(key)
            print(f"\nCustomer {values.customer_id} \nItem {values.item_id} \nCheckout Date {values.checkout_date} \nReturn Date {values.return_date} \nDue Date {values.due_date} \nFines {values.fine}\n")

if __name__ == '__main__':
    unittest.main()