import pymysql.cursors
from database import JuryDatabase

def main():
    db = JuryDatabase('localhost')
    print(db.validateUser('admin', 'pass'))
    print(db.validateUser('admin', 'pass1'))


if __name__ == '__main__':
    main()