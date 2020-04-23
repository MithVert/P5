#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
import importingdatascript as importing
import json

class Sqlmain():
    """WIP"""

    def __init__(self,database = importing.databasename, categories = importing.chosencategories, columns =importing.chosencolumns, credentials = importing.credentialspath):
        self.database = database
        self.categories = categories
        self.columns = columns
        self.credentials = json.load(open(credentials,"r"))
        self.cnx = None

    def connect(self):

        try:
            self.cnx = mysql.connector.connect(**self.credentials, database=self.database)

        except mysql.connector.errors.DatabaseError:
            data = []
            for categorie_name in self.categories:
                categorie = importing.Categorie(categorie_name)
                dataadd = categorie.get()
                data = data.__add__(dataadd)
                sqlbdd = importing.Sqldatacreator(data)
                sqlbdd.createtable()
                sqlbdd.insertdataintotable()
                sqlbdd.disconnect()
            self.cnx = mysql.connector.connect(**self.credentials, database=self.database)
    
    def disconnect(self):
        self.cnx.close()
    
    def listingundercategories(self, categorie):

        undercategories = []

        if self.cnx:
            pass
        else:
            self.connect()

        cur = self.cnx.cursor()
        query = """SELECT categories FROM produits WHERE categorie = "{}" ;""".format(categorie)
        cur.execute(query)

        for categories in cur:
            
            categories_temp = categories[0].split(", ")

            if len(categories_temp) == 1:
                categories_temp = categories[0].split(",")
            
            compt = 0

            for i in range(len(categories_temp)):

                compt = compt + len(categories_temp[i])+2

                if compt >= 198:
                    continue
                else:
                    if ":" in categories_temp[i]:
                        continue
                    elif categories_temp[i] not in undercategories:
                        undercategories.append(categories_temp[i])
        return undercategories
    

if __name__=="__main__":
    sql = Sqlmain()
    sql.listingundercategories("boissons")
    sql.disconnect()