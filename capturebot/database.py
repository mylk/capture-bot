import sqlite3
import time

class Database:
    connection = False

    def __init__(self):
        self.connection = sqlite3.connect("capture_bot.db")

    def store_element(self, element):
        authored = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(element["authored"]))

        query = self.connection.cursor()
        query.execute(
            "INSERT INTO elements (id, type, subreddit, authored) VALUES ('%s', %s, '%s', '%s')"
            % (element["id"], element["type"], element["subreddit"], authored)
        )
        self.connection.commit()

    def element_exists(self, element):
        authored = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(element["authored"]))

        query = self.connection.cursor()
        query.execute(
            "SELECT id FROM elements WHERE id = '%s' AND subreddit = '%s' AND type = %s AND authored = '%s'"
            % (element["id"], element["subreddit"], element["type"], authored)
        )

        return query.fetchone()