import unittest
from item_storage import Book, Book_File, Book_None_Available, Book_Not_Found, Not_A_Book
from os import path

class TestItems(unittest.TestCase):
    book_file = Book_File()
# adding books
    def test_1(self):
        book_1 = Book("The Fellowship of the Ring", "JRR Tolkien", "978-0345339706")
        book_2 = Book("The Fellowship of the Ring", "JRR Tolkien", "978-0345339706")
        book_3 = Book("The Two Towers", "JRR Tolkien", "978-0345339713", 2)
        book_file = TestItems.book_file
        book_file.add_book(book_1)
        book_file.add_book(book_2)
        book_file.add_book(book_3)
        for key, value in book_file.books.items():
            print(f"{key} : {value.details()}")
        self.assertTrue(path.exists(book_file.file_name))
# type error when adding books
    def test_2(self):
        book = 5
        book_file = TestItems.book_file
        with self.assertRaises(Not_A_Book):
            book_file.add_book(book)
# removing books
    def test_3(self):
        book_file = TestItems.book_file
        book_2 = Book("The Fellowship of the Ring", "JRR Tolkien", "978-0345339706")
        book_file.remove_book(book_2)
        book_3 = Book("The Two Towers", "JRR Tolkien", "978-0345339713")
        book_file.remove_book(book_3)
        for key, value in book_file.books.items():
            print(f"{key} : {value.details()}")
        self.assertTrue(path.exists(book_file.file_name))
# book not found error when removing
    def test_4(self):
        book = Book("The Return of the King", "JRR Tolkien", "978-0345339737")
        book_file = TestItems.book_file
        with self.assertRaises(Book_Not_Found):
            book_file.remove_book(book)
# book not available
    def test_5(self):
        book_file = TestItems.book_file
        book_3 = Book("The Two Towers", "JRR Tolkien", "978-0345339713")
        book_file.remove_book(book_3) # remove last copy
        with self.assertRaises(Book_None_Available):
            book_file.remove_book(book_3)

if __name__ == '__main__':
    unittest.main()