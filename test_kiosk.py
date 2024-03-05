from kiosk import Kiosk
import unittest
import datetime
from transaction import Transaction_File

class Customer:
    def __init__(self, name, num) -> None:
        self.id = num
        self.name = name
class Book:
    def __init__(self, num) -> None:
        self.id = num

sample_store = Transaction_File()
class Test(unittest.TestCase):
    def test_checkout1(self):
        customer = Customer("AP", 1)
        item = Book(1)
        kiosk = Kiosk(sample_store)
        receipt = kiosk.checkout_item2(customer, item)
        test_receipt = f"{customer.id} {item.id} 2024-03-05 11:55:14.240788"
        print(f"\n{receipt}\n{test_receipt}\n")
    
    def test_checkout2(self):
        customer = Customer("AP2", 2)
        item = Book(2)
        kiosk = Kiosk(sample_store)
        receipt = kiosk.checkout_item2(customer, item)
        test_receipt = f"{customer.id} {item.id} 2024-03-05 11:55:14.241794"
        print(f"\n{receipt}\n{test_receipt}\n")
    
    def return_item1(self):
        kiosk = Kiosk(sample_store)
        receipt1  = f"1 1 2024-03-05 11:55:14.240788"
        kiosk.return_item(receipt1)
        test_receipt1 = f"1 1 2024-03-05 11:55:14.240788 {datetime.datetime.utcnow()}"
        print(f"\n{receipt1}\n{test_receipt1}\n")
    
    def return_item2(self):
        kiosk = Kiosk(sample_store)
        receipt2  = f"2 2 2024-03-05 11:55:14.241794"
        kiosk.return_item(receipt2)
        test_receipt2 = f"2 2 2024-03-05 11:55:14.241794 {datetime.datetime.utcnow()}"
        print(f"\n{receipt2}\n{test_receipt2}\n")
    
if __name__ == '__main__':
    unittest.main()