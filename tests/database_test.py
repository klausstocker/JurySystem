import unittest
import pymysql.cursors
from frontend.flet.src.database import JuryDatabase, Restrictions, User


class TestDatabase(unittest.TestCase):

    def test_user(self):
        db = JuryDatabase('localhost')
        self.assertTrue(db.validateUser('admin', 'pass'))
        self.assertFalse(db.validateUser('admin', 'pass1'))

        user = db.getUser(1)
        self.assertEqual(user.restrictions, Restrictions.ADMIN)
        self.assertTrue(user.valid())
        
        insertedId = db.insertUser('michelhausen', 'pass', 'michelhausen@sportunion.at', Restrictions.TRAINER)
        insertedUser = db.getUser(insertedId)
        self.assertEqual(insertedUser.username, 'michelhausen')
        self.assertEqual(insertedUser.locked, 0)
        self.assertEqual(insertedUser.restrictions, Restrictions.TRAINER)
        
        self.assertTrue(db.removeUser(insertedId))
        self.assertFalse(db.removeUser(insertedId))


if __name__ == '__main__':
    unittest.main()