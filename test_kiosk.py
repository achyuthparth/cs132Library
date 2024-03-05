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
class TestKiosk(unittest.TestCase):
    cls_r1 = ""
    cls_r2 = ""
    
    def test_checkout1(self):
        customer = Customer("AP", 1)
        item = Book(1)
        kiosk = Kiosk(sample_store)
        receipt = kiosk.checkout_item2(customer, item)
        TestKiosk.cls_r1 = receipt
        test_receipt1 = f"{customer.id} {item.id} {datetime.datetime.utcnow()}"
        print(f"\n{receipt}\n{test_receipt1}\n")
    
    def test_checkout2(self):
        customer = Customer("AP2", 2)
        item = Book(2)
        kiosk = Kiosk(sample_store)
        receipt = kiosk.checkout_item2(customer, item)
        TestKiosk.cls_r2 = receipt
        test_receipt2 = f"{customer.id} {item.id} {datetime.datetime.utcnow()}"
        print(f"\n{receipt}\n{test_receipt2}\n")
    
    def test_return_item1(self):
        kiosk = Kiosk(sample_store)
        #receipt1  = f"1 1 2024-03-05 20:49:56.383287"
        receipt = TestKiosk.cls_r1
        receipt1 = kiosk.return_item(receipt)
        test_receipt = f"{TestKiosk.cls_r1} {datetime.datetime.utcnow()}"
        print(f"\n{receipt1}\n{test_receipt}\n")
    
    def test_return_item2(self):
        kiosk = Kiosk(sample_store)
        #receipt2  = f"2 2 2024-03-05 20:50:26.791286"
        receipt = TestKiosk.cls_r2
        receipt2 = kiosk.return_item(receipt)
        test_receipt = f"{TestKiosk.cls_r2} {datetime.datetime.utcnow()}"
        print(f"\n{receipt2}\n{test_receipt}\n")
    
if __name__ == '__main__':
    unittest.main()