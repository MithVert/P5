#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
import json

class CSVData():
    
    def __init__(self):
        self.mysqldatabase = "openfooddata"
        self.credentials = json.load(open("/home/gery/Documents/OC/P5Global/credentials.json","r"))
        self.categorie = ("boissons","plats-prepares","biscuits-et-gateaux","produits-a-tartiner-sucres","sauces")

    def connect(self):

        """ne fait pas sens au sein de la classe CSVData"""

        self.cnx = mysql.connector.connect(**self.credentials)

    def disconnect(self):

        """ne fait pas sens au sein de la classe CSVData"""

        self.cnx.close()
    
    def tablecreation(self):

        """ne fait pas sens au sein de la classe CSVData"""

        try:
            query = "CREATE DATABASE {}".format(self.mysqldatabase)
            cur = self.cnx.cursor()
            cur.execute(query)
            return True
        except mysql.connector.errors.DatabaseError:
            a = input("Another instance of the database already exists, would you like to overwrite it ? [y/n]")
            if a=="y" or a=="Y":
                query = "DROP DATABASE {}".format(self.mysqldatabase)
                cur = self.cnx.cursor()
                cur.execute(query)
                query = "CREATE DATABASE {}".format(self.mysqldatabase)
                cur.execute(query)
                return True
            else:
                return False




if __name__=="__main__":
    data= CSVData()
    data.connect()
    status = data.tablecreation()
    print(status)
    data.disconnect()