import mysql.connector
import json
from parameters import CREDENTIALSPATH, DATABASENAME


class Sqldatabasemanager():

    def __init__(self):

        self.credentials = json.load(open(CREDENTIALSPATH, "r"))

    def connect(self):

        """Connect to self.database
        If self.database doesn't exist, create it before connecting"""

        try:
            self.cnx = mysql.connector.connect(
                **self.credentials, database=DATABASENAME)

        except mysql.connector.errors.DatabaseError:
            self.cnx = mysql.connector.connect(**self.credentials)
            self.createdatabase()

    def createdatabase(self):

        """Create the database DATABASENAME and connect to it
        Should only be called by <self.connect>"""

        query = f"CREATE DATABASE `{DATABASENAME}`"
        cur = self.cnx.cursor()
        cur.execute(query)
        self.cnx.commit()
        self.cnx.close()
        self.connect()

    def disconnect(self):

        self.cnx.close()

    def drop(self):

        """Delete the local database <self.database>
        Should only be called by self.loaddata()"""

        if self.cnx:
            pass
        else:
            self.connect()

        cur = self.cnx.cursor()
        query = f"DROP DATABASE {DATABASENAME}"
        cur.execute(query)

    def load(self, data):

        """load all the data to the MySQL Database"""
