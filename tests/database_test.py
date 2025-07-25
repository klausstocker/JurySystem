import os
import sys
import unittest
import pymysql.cursors
from shared.database import JuryDatabase, Restrictions, User, Gender, EventCategory, RankingType
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
        self.assertEqual(len(self.db.getEventGroup(1, 'Riege2')), 2)
        self.assertEqual(len(self.db.getEventCategoryAthleteIds(1, 'Kn01')), 3)
        self.assertEqual(self.db.getEventCategories(1)[0].name, 'Kn01')
    
    def test_rating(self):
        self.assertEqual(len(self.db.getEventRatings(1, 1)), 1)
        self.assertEqual(len(self.db.getEventRatings(1, 2)), 2)
        self.assertAlmostEqual(float(self.db.getAthleteAndRatings(1, 1).sum()), 14.7)
        insertedId = self.db.insertRating(2, 1, 5, 'Sprung', 2., 3.)
        self.assertAlmostEqual(float(self.db.getAthleteAndRatings(2, 1).sum()), 19.7)
        self.assertIsNotNone(self.db.updateRating(insertedId, 5, 3., 4.))
        self.assertAlmostEqual(float(self.db.getAthleteAndRatings(2, 1).sum()), 21.7)
        self.db.removeRating(insertedId)
        rankings = self.db.getEventCategoryRankings(1, 'Kn01')
        self.assertEqual(rankings[0].ratings.athlete.givenname, 'Klaus')
        self.assertEqual(rankings[0].ranking, '1')
        self.assertEqual(rankings[1].ratings.athlete.givenname, 'Christoph')
        self.assertEqual(rankings[1].ranking, '1')
        self.assertEqual(rankings[2].ranking, '2')
        norankings = self.db._getEventCategoryRankings(1, \
            EventCategory('Kn01', 1, Gender.MALE, '01-01-2000', '31-12-2001', \
                RankingType.NO_RANKING, EventCategory.defaultRankingAlgo()))
        self.assertEqual(norankings[0].ratings.athlete.givenname, 'Klaus')
        self.assertEqual(norankings[0].ranking, 'bronze')


if __name__ == '__main__':
    unittest.main()