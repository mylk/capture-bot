import sqlite3
import time

class Database:
    connection = False

    def __init__(self):
        self.connection = sqlite3.connect("capture_bot.db")

    def store_element(self, element):
        element_authored = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(element.created_utc))

        query = self.connection.cursor()
        query.execute(
            "INSERT INTO elements (id, type, subreddit, authored) VALUES ('%s', %s, '%s', '%s')"
            % (element.id, element.element_type, element.subreddit, element_authored)
        )
        self.connection.commit()

    def element_exists(self, element):
        element_authored = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(element.created_utc))

        query = self.connection.cursor()
        query.execute(
            "SELECT id FROM elements WHERE id = '%s' AND type = %s AND subreddit = '%s' AND authored = '%s'"
            % (element.id, element.element_type, element.subreddit, element_authored)
        )

        return query.fetchone()