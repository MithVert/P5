import mysql.connector
import json
from parameters import (
    CREDENTIALSPATH, DATABASENAME, CHOSENCOLUMNS, VARCHARLENGHT
)


class Sqldatabasemanager():

    """Class used to dialog with MySQL, it establishes the connection to MySQL
    and, if necessary, it creates the database back from scratch.
    You can get the connexion to MySQL it sets up by getting self.cnx"""

    def __init__(self):

        self.credentials = json.load(open(CREDENTIALSPATH, "r"))
        self.cnx = None

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
        Should only be called by self.connect()"""

        query = f"CREATE DATABASE `{DATABASENAME}`"
        cur = self.cnx.cursor()
        cur.execute(query)
        self.cnx.commit()
        query = f"USE {DATABASENAME};"
        cur = self.cnx.cursor()
        cur.execute(query)
        self.cnx.commit()

        self.createtableproducts()
        self.createtablesubstitutes()
        self.createtablecategories()
        self.createtablerelations()

    def createtableproducts(self):

        """Create the table <Products> where every product is referenced
        Should only be called by self.createdatabase()"""

        table = (
            "CREATE TABLE `Products` ( `id` SMALLINT AUTO_INCREMENT, "
            "`idmaincat` SMALLINT, "
        )

        for s in CHOSENCOLUMNS:

            table = (
                table + f"`{s}` VARCHAR({VARCHARLENGHT}), "
            )

        table = (
            table
            + "PRIMARY KEY(`id`)) CHARACTER SET=utf8mb4 ENGINE=InnoDB;"
        )
        cur = self.cnx.cursor()
        cur.execute(table)
        self.cnx.commit()

    def createtablesubstitutes(self):

        """Create the <Substitutes> table where every substitue id is referenced
        Should only be called by self.createdatabase()"""

        table = (
            "CREATE TABLE `Substitutes` ( `idp` SMALLINT, "
            "FOREIGN KEY(`idp`) REFERENCES `Products`(`id`), "
            "PRIMARY KEY(`idp`)) CHARACTER SET=utf8mb4 ENGINE=InnoDB;"
        )
        cur = self.cnx.cursor()
        cur.execute(table)
        self.cnx.commit()

    def createtablecategories(self):

        """Create the <Categories> table
        where every categorie is referenceded
        Should only be called by self.createdatabase()"""

        table = (
            "CREATE TABLE `Categories` ( `id` SMALLINT, "
            f"`Categorie` VARCHAR({VARCHARLENGHT}), "
            "PRIMARY KEY(`id`)) CHARACTER SET=utf8mb4 ENGINE=InnoDB;"
        )
        cur = self.cnx.cursor()
        cur.execute(table)
        self.cnx.commit()

    def createtablerelations(self):

        """Create the <Relations> table where we link the products
        to the categorie(s) they have"""

        table = (
            "CREATE TABLE `Relations` ( `idp` SMALLINT, `idc` SMALLINT, "
            "FOREIGN KEY (`idp`) REFERENCES Products(`id`), "
            "FOREIGN KEY (`idp`) REFERENCES Products(`id`), "
            "PRIMARY KEY (`idp`,`idc`)) "
            "CHARACTER SET=utf8mb4 ENGINE=InnoDB;"
        )
        cur = self.cnx.cursor()
        cur.execute(table)
        self.cnx.commit()

    def disconnect(self):

        self.cnx.close()

    def drop(self):

        """Delete the local database DATABASENAME
        Use with cautious"""

        if self.cnx:
            pass
        else:
            self.connect()

        cur = self.cnx.cursor()
        query = f"DROP DATABASE {DATABASENAME}"
        cur.execute(query)
