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
        receipt = kiosk.checkout_item(customer, item)
        test_receipt = f"{item.id} {customer.id} {datetime.datetime.utcnow()}"
        print(f"{receipt}\n{test_receipt}")
    
    def test_checkout2(self):
        customer = Customer("AP2", 2)
        item = Book(2)
        kiosk = Kiosk(sample_store)
        receipt = kiosk.checkout_item(customer, item)
        test_receipt = f"{item.id} {customer.id} {datetime.datetime.utcnow()}"
        print(f"{receipt}\n{test_receipt}")
    
if __name__ == '__main__':
    unittest.main()