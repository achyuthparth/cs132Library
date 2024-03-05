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
        test_receipt = tuple(map(str, (item.id, customer.id, datetime.datetime.utcnow())))
        self.assertAlmostEqual(test_receipt,receipt)
    
if __name__ == '__main__':
    unittest.main()