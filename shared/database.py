import pymysql.cursors
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List

class Restrictions(Enum):
    TRAINER = 0
    HOST = 1
    JUDGE = 2
    ADMIN = 3
    
class Gender(Enum):
    MALE = 0
    FEMALE = 1
    
class RankingType(Enum):
    NO_RANKING = 1
    RANKING = 0

@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    team: str
    registered: datetime
    expires: datetime
    restrictions: Restrictions
    locked: bool
    hidden: bool
    
    def valid(self) -> bool:
        return datetime.now() < self.expires and not self.locked
    
    @staticmethod
    def fromRow(row):
        return User(row['id'], row['username'], row['password'], row['email'], row['team'], row['registered'], row['expires'], Restrictions(row['restrictions']), row['locked'] != 0, row['hidden'] != 0)


@dataclass
class Athlete:
    id: int
    givenname: str
    surname: str
    userId: int
    birth: datetime
    gender: Gender
    hidden: bool
    
    @staticmethod
    def fromRow(row):
        return Athlete(row['id'], row['givenname'], row['surname'], row['userId'], row['birth'], Gender(row['gender']), row['hidden'] != 0)
    
    def name(self):
        return f'{self.givenname} {self.surname}'
    
    def birthFormated(self):
        return self.birth.strftime('%d.%m.%Y')

    @staticmethod
    def birthFromString(birth: str):
        return datetime.strptime(birth, '%d.%m.%Y')

class Progress(Enum):
    PLANNED = 0
    ACTIVE = 1
    FINISHED = 2
    DELETED = 3
@dataclass
class Event:
    id: int
    name: str
    userId: int
    date: datetime
    progress: Progress

    @staticmethod
    def fromRow(row):
        return Event(row['id'], row['name'], row['userId'], row['date'], Progress(row['progress']))

    def dateFormated(self):
        return self.date.strftime('%d.%m.%Y')

@dataclass
class EventCategory:
    name: str
    eventId: int
    gender: Gender
    birthFrom: datetime
    birthTo: datetime
    rankingType: RankingType
    rankingAlgo: str

    @staticmethod
    def fromRow(row):
        return EventCategory(row['name'], row['eventId'], Gender(row['gender']), row['birthFrom'], row['birthTo'], RankingType(row['rankingType']), row['rankingAlgo'])

    @staticmethod
    def defaultRankingAlgo():
        return "'gold' if sum > 30 else 'silber' if sum > 20 else 'bronze' if sum > 10 else ''"

@dataclass
class EventDiscipline:
    name: str
    eventId: int
    
    @staticmethod
    def fromRow(row):
        return EventDiscipline(row['name'], row['eventId'])

@dataclass
class Attendance:
    athleteId: int
    eventId: int
    eventCategoryName: str
    
    @staticmethod
    def fromRow(row):
        return Attendance(row['athleteId'], row['eventId'], row['eventCategoryName'])

@dataclass
class Rating:
    id: int
    ts: datetime
    athleteId: int
    eventId: int
    userId: int
    eventDisciplineName: str
    difficulty: float
    execution: float
    
    def sum(self):
        return self.difficulty + self.execution
    
    def pretty(self):
        return '{:.2f}'.format(self.difficulty), '{:.2f}'.format(self.execution)
    
    def rate(self, difficulty: float, execution: float):
        self.ts = datetime.now()
        self.difficulty = difficulty
        self.execution = execution
    
    @staticmethod
    def fromRow(row):
        return Rating(row['id'], row['ts'], row['athleteId'], row['eventId'], row['userId'], row['eventDisciplineName'], row['difficulty'], row['execution'])

@dataclass
class AthleteRatings:
    athlete: Athlete
    eventId: int
    eventCategoryName: str
    ratings: dict[str, Rating]
    
    def sum(self):
        return sum(r.sum() for r in self.ratings.values())
    
    def ratingOrNone(self, discpiline: str):
        if discpiline in self.ratings.keys():
            return self.ratings[discpiline].difficulty, self.ratings[discpiline].execution, self.ratings[discpiline].id
        return None, None, None

@dataclass
class AthleteRanking:
    ranking: str
    ratings: AthleteRatings

class JuryDatabase:
    def __init__(self, host: str, autocommit=False):
        self.conn = pymysql.connect(host=host,
                            user='JurySystem',
                            password='asdfuas347lkasudhr',
                            database='JurySystem',
                            cursorclass=pymysql.cursors.DictCursor,
                            autocommit=autocommit)
        
    def __del__(self):
        self.conn.close()
    
    def validateUser(self, username, password):
        with self.conn.cursor() as cursor:
           if cursor.execute(f'SELECT * FROM users WHERE username="{username}";') != 1:
               return None
           row = cursor.fetchone()
           user = User.fromRow(row)
           if user.password != password and user.valid():
               return None
           return user.id

    def getUser(self, userId: int) -> User:
        with self.conn.cursor() as cursor:
            sql = f'SELECT * FROM users WHERE id="{userId}";'
            cursor.execute(sql)
            return User.fromRow(cursor.fetchone())
        return None

    def insertUser(self, username: str, password: str, email:str, team:str, restrictions: Restrictions) -> int:
        locked = 0
        with self.conn.cursor() as cursor:
            sql = f"INSERT INTO users (username, password, email, team, registered, expires, restrictions, locked) VALUES ('{username}', '{password}', '{email}','{team}', '{datetime.now()}', '{datetime.now() + timedelta(weeks=300)}', {restrictions.value}, {locked});"
            cnt = cursor.execute(sql)
            if cnt != 1:
                return None
            self.conn.commit()
            return cursor.lastrowid
        return None
    
    def removeUser(self, userId: int) -> bool:
        with self.conn.cursor() as cursor:
            sql = f"DELETE FROM `users` WHERE `users`.`id` = {userId} ;"
            cnt = cursor.execute(sql)
            self.conn.commit()
            return cnt != 0
        return False
    
    def updateUser(self, userId: int, username: str, password: str, email: str, team: str, expires: datetime, restrictions: Restrictions, locked: bool):
        with self.conn.cursor() as cursor:
            sql = f"UPDATE `users` SET `username` = '{username}',`password` = '{password}', `email` = '{email}', `team` = '{team}', `expires` = '{expires}',`restrictions` = '{restrictions.value}', `locked` = '{1 if locked else 0}' WHERE `users`.`id` = {userId};"
            cnt = cursor.execute(sql)
            self.conn.commit()
            return cnt != 0
        return False
    
    def getAllUsers(self) -> List[User]:
        users = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE hidden = 0;')
            for row in cursor.fetchall():
                users.append(User.fromRow(row))
        return users
    
    def getAthletes(self, userId: int) -> List[Athlete]:
        athletes = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM athletes WHERE userId = {userId} AND hidden = 0;')
            for row in cursor.fetchall():
                athletes.append(Athlete.fromRow(row))
        return athletes
    
    def getAthlete(self, athleteId: int) -> Athlete:
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM athletes WHERE id = {athleteId};')
            return Athlete.fromRow(cursor.fetchone())
        return None
    
    def insertAthlete(self, givenname: str, surname: str, userId: int, birth: datetime, gender: Gender):
        with self.conn.cursor() as cursor:
            sql = f"INSERT INTO athletes (givenname, surname, userId, birth, gender) VALUES ('{givenname}', '{surname}', '{userId}','{birth}', {gender.value});"
            cnt = cursor.execute(sql)
            if cnt != 1:
                return None
            self.conn.commit()
            return cursor.lastrowid
        return None

    def updateAthlete(self, athleteId: int,  givenname: str, surname: str, userId: int, birth: datetime, gender: Gender):
        with self.conn.cursor() as cursor:
            sql = f"UPDATE `athletes` SET `givenname` = '{givenname}',`surname` = '{surname}', `userId` = '{userId}', `birth` = '{birth}', `gender` = {gender.value} WHERE `athletes`.`id` = {athleteId};"
            cnt = cursor.execute(sql)
            self.conn.commit()
            return cnt != 0
        return False

    def athleteHasAttendances(self, athleteId):
        with self.conn.cursor() as cursor:
            sql = f"SELECT * FROM `attendances` WHERE `athleteId` = {athleteId} ;"
            return cursor.execute(sql) != 0
        return False
    
    def hideAthlete(self, athleteId: int, hide: bool):
        with self.conn.cursor() as cursor:
            sql = f"UPDATE `athletes` SET `hidden` = {1 if hide else 0} WHERE `athletes`.`id` = {athleteId};"
            cursor.execute(sql)
            self.conn.commit()

    def removeAthlete(self, athleteId: int) -> bool:
        """An athlete can only be deleted if there are no attendancies any more, 
            otherwise he can only be hidden."""
        if self.athleteHasAttendances(athleteId):
            self.hideAthlete(athleteId, True)
        else:
            with self.conn.cursor() as cursor:
                sql = f"DELETE FROM `athletes` WHERE `athletes`.`id` = {athleteId} ;"
                cnt = cursor.execute(sql)
                self.conn.commit()
                return cnt != 0
        return False
    
    def getEvents(self, userId: int) -> List[Event]:
        events = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM events WHERE userId = {userId};')
            for row in cursor.fetchall():
                events.append(Event.fromRow(row))
        return events
    
    def getAllEvents(self) -> List[Event]:
        events = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM events;')
            for row in cursor.fetchall():
                events.append(Event.fromRow(row))
        return events
    
    def getEvent(self, eventId: int) -> Event:
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM events WHERE id = {eventId};')
            return Event.fromRow(cursor.fetchone())
        return None
    
    def insertEvent(self, name: str, userId: int, date: datetime):
        with self.conn.cursor() as cursor:
            sql = f"INSERT INTO events (name, userId, date) VALUES ('{name}', '{userId}', '{date}');"
            cnt = cursor.execute(sql)
            if cnt != 1:
                return None
            self.conn.commit()
            return cursor.lastrowid
        return None

    def updateEvent(self, eventId: int,  name: str, userId: int, date: datetime):
        with self.conn.cursor() as cursor:
            sql = f"UPDATE `events` SET `name` = '{name}', `userId` = '{userId}', `date` = '{date}' WHERE `events`.`id` = {eventId};"
            cnt = cursor.execute(sql)
            self.conn.commit()
            return cnt != 0
        return False

    def removeEvent(self, eventId: int) -> bool:
        with self.conn.cursor() as cursor:
            sql = f"DELETE FROM `events` WHERE `events`.`id` = {eventId} ;"
            cnt = cursor.execute(sql)
            self.conn.commit()
            return cnt != 0
        return False
    
    def getEventCategory(self, eventId: int, eventCategoryName: str) -> EventCategory:
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM `event_categories` WHERE `eventId` = {eventId} AND `name`= "{eventCategoryName}";')
            return EventCategory.fromRow(cursor.fetchone())
        return None
    
    def getAttendance(self, athleteId: int, eventId: int) -> Attendance:
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM attendances WHERE athleteId = {athleteId} AND eventId = {eventId};')
            return Attendance.fromRow(cursor.fetchone())
        return None
    
    def getEventCategoryAthleteIds(self, eventId: int, eventCategoryName: str) -> list[int]:
        athleteIds = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT `athleteId` FROM `attendances` WHERE `eventId` = {eventId} AND `eventCategoryName` = "{eventCategoryName}";')
            for row in cursor.fetchall():
                athleteIds.append(int(row['athleteId']))
        return athleteIds
    
    def getEventRatings(self, eventId: int, max: int) -> list[Rating]:
        ratings = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM ratings WHERE eventId = {eventId} ORDER BY id DESC LIMIT {max};')
            for row in cursor.fetchall():
                ratings.append(Rating.fromRow(row))
        return ratings
    
    def getRecentRatingTs(self, eventId: int) -> datetime:
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT MAX(`ts`) as maxTs FROM `ratings`;')
            return cursor.fetchone()['maxTs']
        return None

    def getEventDisciplines(self, eventId: int) -> list[EventDiscipline]:
        disciplines = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM `event_disciplines` WHERE eventId = {eventId} ORDER BY name;')
            for row in cursor.fetchall():
                disciplines.append(EventDiscipline.fromRow(row))
        return disciplines

    def getEventCategories(self, eventId: int) -> list[EventCategory]:
        categories = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM `event_categories` WHERE eventId = {eventId} ORDER BY name;')
            for row in cursor.fetchall():
                categories.append(EventCategory.fromRow(row))
        return categories

    def getEventGroups(self, eventId: int) -> list[str]:
        groups = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT DISTINCT `group` FROM `attendances` WHERE eventId = {eventId} ORDER BY `group`;')
            for row in cursor.fetchall():
                groups.append(row['group'])
        return groups
    
    def getEventGroup(self, eventId: int, group: str) -> list[Athlete]:
        athletes = []
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT `athletes`.* FROM `attendances` JOIN `athletes` ON athletes.id=attendances.athleteId WHERE `attendances`.`eventId` = {eventId} AND `attendances`.`group` = "{group}";')
            for row in cursor.fetchall():
                athletes.append(Athlete.fromRow(row))
        return athletes


    def getAthleteRatings(self, athleteId: int, eventId: int) -> list[Rating]:
        ratings = {}
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM `ratings` WHERE `eventId` = {eventId} AND `athleteId` = "{athleteId}";')
            for row in cursor.fetchall():
                rating = Rating.fromRow(row)
                ratings[rating.eventDisciplineName] = rating
        return ratings

    def getAthleteAndRatings(self, athleteId: int, eventId: int) -> AthleteRatings:
        athlete = self.getAthlete(athleteId)
        attendance = self.getAttendance(athleteId, eventId)
        return AthleteRatings(athlete, eventId, attendance.eventCategoryName, self.getAthleteRatings(athleteId, eventId))

    def _getEventCategoryRankings(self, eventId, category: EventCategory) -> list[AthleteRanking]:
        rankings = []
        ratings = [self.getAthleteAndRatings(athleteId, eventId) for athleteId in self.getEventCategoryAthleteIds(eventId, category.name)]
        ratings.sort(key=lambda rating: rating.sum(), reverse=True)
        if category.rankingType == RankingType.RANKING:
            rank = 0
            sum = -1.
            for rating in ratings:
                ratingSum = round(rating.sum(), 6)
                if ratingSum == 0.0:
                    rankings.append(AthleteRanking('DNF', rating))
                else:
                    if ratingSum != sum:
                        rank += 1
                    sum = ratingSum
                    rankings.append(AthleteRanking(str(rank), rating))
        elif category.rankingType == RankingType.NO_RANKING:
            for rating in ratings:
                ratingSum = round(rating.sum(), 6)
                if ratingSum == 0.0:
                    rankings.append(AthleteRanking('DNF', rating))
                else:
                    rankings.append(AthleteRanking(eval(category.rankingAlgo, {}, {'sum':ratingSum}), rating))
        return rankings

    def getEventCategoryRankings(self, eventId: int, eventCategoryName: str) -> list[AthleteRanking]:
        category = self.getEventCategory(eventId, eventCategoryName)
        return self._getEventCategoryRankings(eventId, category)


    def updateRating(self, ratingId: int, userId: int, difficulty: float, execution: float):
        with self.conn.cursor() as cursor:
            sql = f"UPDATE `ratings` SET`ts`='{datetime.now()}', `userId`='{userId}', `difficulty`='{difficulty}', `execution`='{execution}' WHERE `id`='{ratingId}'"
            cnt = cursor.execute(sql)
            if cnt != 1:
                return None
            self.conn.commit()
            return cursor.lastrowid
        return None

    def insertRating(self, athleteId: int, eventId: int, userId: int, eventDisciplineName: str, difficulty: float, execution: float):
        with self.conn.cursor() as cursor:
            sql = f"INSERT INTO `ratings` (athleteId, eventId, ts, userId, eventDisciplineName, difficulty, execution) VALUES ('{athleteId}', '{eventId}', '{datetime.now()}', '{userId}', '{eventDisciplineName}', '{difficulty}', '{execution}');"
            cnt = cursor.execute(sql)
            if cnt != 1:
                return None
            self.conn.commit()
            return cursor.lastrowid
        return None
    
    def removeRating(self, ratingId: int):
        with self.conn.cursor() as cursor:
            sql = f"DELETE FROM `ratings` WHERE `ratings`.`id` = '{ratingId}';"
            cnt = cursor.execute(sql)
            self.conn.commit()
            return cnt != 0
        return False
