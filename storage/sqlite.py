from sqlite3 import connect, Error

from storage.base_storage import Storage


class SQLiteStorage(Storage):

    _database = None

    def __init__(self, database_name):
        try:
           self._database = connect(database_name, check_same_thread=False)
        except Error as e:
            print("Database error: %s" %e)

    def execute(self, command: str):
        cur = self._database.cursor()
        cur.execute(command)
        cur.close()
        self._database.commit()

    def fetch(self, command: str):
        cur = self._database.cursor()
        cur.execute(command)
        result = cur.fetchall()
        cur.close()
        return result
