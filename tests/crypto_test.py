import bcrypt
import unittest

class TestCrypto(unittest.TestCase):

    def test_hashpw(self):
        hash1 = bcrypt.hashpw('pass'.encode(), bcrypt.gensalt())
        hash2 = bcrypt.hashpw('pass'.encode(), bcrypt.gensalt())
        self.assertNotEqual(hash1, hash2)
        self.assertTrue(bcrypt.checkpw('pass'.encode(), hash1))
        self.assertTrue(bcrypt.checkpw('pass'.encode(), hash2))
        
if __name__ == '__main__':
    unittest.main()