import os
import sys
import unittest
import pymysql.cursors
from shared.database import JuryDatabase, Restrictions, User, Gender
from datetime import datetime


class TestDatabase(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.db = JuryDatabase('localhost')
        
    def test_restrictions(self):
        a = Restrictions['TRAINER']
        self.assertEqual(a, Restrictions.TRAINER)

    def test_user(self):
        self.assertTrue(self.db.validateUser('admin', 'pass'))
        self.assertFalse(self.db.validateUser('admin', 'pass1'))

        user = self.db.getUser(1)
        self.assertEqual(user.restrictions, Restrictions.ADMIN)
        self.assertTrue(user.valid())
        
        insertedId = self.db.insertUser('judenau', 'pass', 'judena@sportunion.at', '', Restrictions.TRAINER)
        insertedUser = self.db.getUser(insertedId)
        self.assertEqual(insertedUser.username, 'judenau')
        self.assertEqual(insertedUser.locked, 0)
        self.assertEqual(insertedUser.restrictions, Restrictions.TRAINER)
        self.assertTrue(self.db.updateUser(insertedId, 'judenau1', 'pass', '', '', datetime.now(), Restrictions.TRAINER, False))
        self.assertEqual(self.db.getUser(insertedId).username, 'judenau1')
        
        self.assertTrue(self.db.removeUser(insertedId))
        self.assertFalse(self.db.removeUser(insertedId))
        
    def test_athlete(self):
        athletes = self.db.getAthletes(3)
        self.assertEqual(len(athletes), 2)
        self.assertEqual(athletes[0].givenname, 'Klaus')
        self.assertTrue(self.db.athleteHasAttendances(3))
        self.assertFalse(self.db.athleteHasAttendances(4))
        
        insertedId = self.db.insertAthlete('Daniel', 'Stocker', 3, '2015-03-31', Gender.MALE)
        self.assertEqual(self.db.getAthlete(insertedId).givenname, 'Daniel')
        self.assertTrue(self.db.updateAthlete(insertedId, 'Daniel', 'Stocker1', 3, '2015-03-31', Gender.MALE))
        self.assertEqual(self.db.getAthlete(insertedId).surname, 'Stocker1')
        self.assertTrue(self.db.removeAthlete(insertedId))
        
        self.db.removeAthlete(3)
        self.assertTrue(self.db.getAthlete(3).hidden)
        self.db.hideAthlete(3, False)
        self.assertFalse(self.db.getAthlete(3).hidden)


    def test_events(self):
        events = self.db.getEvents(2)
        self.assertEqual(events[0].name, 'Bezirksmeisterschaften 2025')
        insertedId = self.db.insertEvent('LM', 2, '2026-01-01')
        self.assertTrue(self.db.updateEvent(insertedId, 'LM1', 2, '2026-01-02'))
        self.assertEqual(self.db.getEvent(insertedId).name, 'LM1')
        self.assertTrue(self.db.removeEvent(insertedId))
        self.assertEqual(len(self.db.getEventDisciplines(1)), 4)
        self.assertEqual(len(self.db.getEventGroups(1)), 2)
        self.assertEqual(len(self.db.getEventGroup(1, 'Riege1')), 2)
        self.assertEqual(len(self.db.getEventGroup(1, 'Riege2')), 1)
    
    def test_rating(self):
        self.assertEqual(len(self.db.getEventRatings(1, 1)), 1)
        self.assertEqual(len(self.db.getEventRatings(1, 2)), 2)
        
        
if __name__ == '__main__':
    unittest.main()