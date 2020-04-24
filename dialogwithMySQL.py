import mysql.connector
import json
from parameters import *
from langdetect import detect, DetectorFactory
from dialogwithOFFAPI import *
DetectorFactory.seed = 0

class Sqldatacreator():

    """class uploading data stored as list of dictionnaries in sql database in a main TABLE"""

    def __init__(self,data,database=databasename, credentials = credentialspath, columns = chosencolumns):
        self.columns = columns
        self.data = data
        self.database = database
        self.credentials = json.load(open(credentials,"r"))
        self.cnx = None
    
    def connect(self):

        """connect to self.database, if self.database doesn't exist, create it before connecting"""

        try:
            self.cnx = mysql.connector.connect(**self.credentials, database=self.database)

        except mysql.connector.errors.DatabaseError:
            self.cnx = mysql.connector.connect(**self.credentials)
            query = "CREATE DATABASE {} CHARACTER SET utf8".format(self.database)
            cur = self.cnx.cursor()
            cur.execute(query)
            query = "USE {}".format(self.database)
            cur.execute(query)
        
    
    def disconnect(self):

        self.cnx.close()

    def createtable(self):

        if self.cnx :
            pass
        else:
            self.connect()
        
        try:
            table = "CREATE TABLE `produits` ( `id` SMALLINT AUTO_INCREMENT, "

            for s in self.columns:
                table = table + "`{}` VARCHAR(200), ".format(s)
            table = table + "PRIMARY KEY(`id`)) ENGINE=InnoDB;"
            cur = self.cnx.cursor()
            cur.execute(table)
        except mysql.connector.errors.Error as err:
            if str(err) == "1050 (42S01): Table 'produits' already exists":
                pass
            else:
                raise err
        

    def insertdataintotable(self):

        if self.cnx :
            pass
        else:
            self.connect()

        cur = self.cnx.cursor()

        print("Saving data to MySQL :\t",end="\n\t\t\t\t\t")

        columnstr = "("
        valuestr = " VALUES ("
        for c in self.columns:
            columnstr = columnstr + c +", "
            valuestr = valuestr + "%({})s, ".format(c)
        columnstr = columnstr[:-2]+")"
        valuestr = valuestr[:-2]+")"
        
        for pdt in self.data:
            addpdt = "INSERT INTO produits " + columnstr + valuestr + ";"
            cur.execute(addpdt,pdt)
            self.cnx.commit()
        cur.close()
        print("Done")

class Sqlmain():
    """Class creating subtables and sorting them"""

    def __init__(self,database = databasename, categories = chosencategories, columns =chosencolumns, credentials = credentialspath):
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
                categorie = Categorie(categorie_name)
                dataadd = categorie.get()
                data = data.__add__(dataadd)
                sqlbdd = Sqldatacreator(data)
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