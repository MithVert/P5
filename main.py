#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
import importingdatascript as importing
import json
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

def dashtounderscore(string):
    """takes string, return new string where "-" has been replaced by "_" """
    string_temp = ""
    for i in string:
        if i == "-":
            string_temp = string_temp + "_"
        else:
            string_temp = string_temp + i
    return string_temp

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

        """ returns a list of all the subcategories the products of a main<categorie> have """

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
                    elif categories_temp[i] not in undercategories and detect(categories_temp[i])=="fr":
                        undercategories.append(categories_temp[i])

        return undercategories
    
    def createcategorietables(self):

        if self.cnx:
            pass
        else:
            self.connect()

        for categorie in self.categories:
            cur = self.cnx.cursor()
            try:
                query = "CREATE TABLE `Table_{}` ( `id` SMALLINT AUTO_INCREMENT, `{}` VARCHAR(50), PRIMARY KEY(`id`))".format(categorie,categorie)
                cur.execute(query)
            except mysql.connector.errors.Error as err:
                if str(err) == "1050 (42S01): Table 'Table_{}' already exists".format(categorie):
                    pass
                else:
                    raise err
            datatoinsert = self.listingundercategories(categorie)
            for data in datatoinsert:
                query = "INSERT INTO Table_{} ({}) VALUES (".format(categorie, categorie)+"%s)"
                cur.execute(query,[data])


    

if __name__=="__main__":
    pass