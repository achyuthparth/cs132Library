from users import User, User_File, Not_A_User, User_Already_Exists, User_Not_Found
import unittest

class Test_Patrons(unittest.TestCase):
    store = User_File()
# add_patron1
    def test_1(self):
        patron_1 = User("AP", "avp6235@psu.edu", "+1-425-393-8472", 1)
        patron_file = self.store
        patron_test = patron_file.add_user(patron_1)
        self.assertTrue(patron_test)
# add_patron2
    def test_2(self): 
        patron_2 = User("AP2", "achyuthaa@outlook.com", "425-393-8472", 2)
        patron_file = self.store
        patron_test = patron_file.add_user(patron_2)
        self.assertTrue(patron_test)
# remove_patron2
    def test_3(self): 
        patron_2 = User("AP2", "achyuthaa@outlook.com", "425-393-8472", 2)
        patron_file = self.store
        patron_test = patron_file.remove_user(patron_2)
        self.assertFalse(patron_test)
# fail_add_patron_exists
    def test_4(self): 
        patron_1 = User("AP", "avp6235@psu.edu", "+1-425-393-8472", 1)
        patron_file = self.store
        with self.assertRaises(User_Already_Exists):
            patron_file.add_user(patron_1)
# fail_add_patron_type_error
    def test_5(self): 
        patron_1 = 5
        patron_file = self.store
        with self.assertRaises(Not_A_User):
            patron_file.add_user(patron_1)
# fail_remove_patron_type_error
    def test_6(self): 
        patron_1 = 1
        patron_file = self.store
        with self.assertRaises(Not_A_User):
            patron_file.remove_user(patron_1)
# fail_remove_patron_already_removed
    def test_7(self):
        patron_2 = User("AP2", "achyuthaa@outlook.com", "425-393-8472", 2)
        patron_file = self.store
        with self.assertRaises(User_Not_Found):
            patron_file.remove_user(patron_2)
# add role

# remove role

# add role type error

# remove role type error

if __name__ == "__main__":
    unittest.main()