import mysql.connector
import json
from parameters import *
from langdetect import detect, DetectorFactory
from dialogwithOFFAPI import *
from utilityfonctions import *
DetectorFactory.seed = 0

class Sqldatabase():

    """Class used to dialog with MySQL local database | only get-, insertsubstitute and loaddata methods should be called outside of the Class"""

    def __init__(self,data=[],database=databasename, credentials = credentialspath, columns = chosencolumns, categories = chosencategories):
        
        self.columns = columns
        self.columnsasstr = "id, "
        for i in self.columns:
            self.columnsasstr = self.columnsasstr + i + ", "
        self.columnsasstr = self.columnsasstr[:-2]
        self.data = data
        self.database = database
        self.credentials = json.load(open(credentials,"r"))
        self.cnx = None
        self.categories = categories
    
    def connect(self):

        """Connect to self.database, if self.database doesn't exist, create it before connecting"""

        try:
            self.cnx = mysql.connector.connect(**self.credentials, database=self.database)

        except mysql.connector.errors.DatabaseError:
            self.cnx = mysql.connector.connect(**self.credentials)
            self.createdatabase()
    
    def createdatabase(self):

        """Create the database <self.database> and connect to it | Should only be called by <self.connect>"""

        query = "CREATE DATABASE `{}`".format(self.database)
        cur = self.cnx.cursor()
        cur.execute(query)
        self.cnx.commit()
        self.cnx.close()
        self.connect()
    
    def disconnect(self):

        """Close the connexion to MySQL server"""

        self.cnx.close()

    def createglobaltable(self):

        """Create the global table <Products> where every product is referenced"""
        
        table = "CREATE TABLE `Products` ( `id` SMALLINT AUTO_INCREMENT, "

        for s in self.columns:
            table = table + "`{}` VARCHAR({}), ".format(s,varchar_length)
        table = table + "PRIMARY KEY(`id`)) ENGINE=InnoDB;"
        cur = self.cnx.cursor()
        cur.execute(table)
        

    def insertdataintoglobaltable(self):

        """Saves <self.data> in the global table <Products> in MySQL"""

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
            addpdt = "INSERT INTO Products " + columnstr + valuestr + ";"
            cur.execute(addpdt,pdt)
            self.cnx.commit()
        cur.close()
        print("Done")
    
    def listingsubcategories(self, categorie):

        """ Returns a list of (<subcategories>,<Nb of occurences of the subcategorie>) among the products where categorie=<categorie> """

        subcat = []
        subcatcount = []

        cur = self.cnx.cursor()
        query = """SELECT categories FROM Products WHERE categorie = "{}";""".format(underscoretodash(categorie))
        cur.execute(query)

        for cat in cur:
            
            cat_1 = cat[0].split(", ")

            for i in range(len(cat_1)):
                if not cat_1[i]:
                    pass
                elif ":" in cat_1[i]:
                    continue
                elif "," in cat_1[i]:
                    cat_2 = cat_1[i].split(",")
                    for j in range(len(cat_2)):
                        if not cat_2[j]:
                            pass
                        elif cat_2[j] in subcat:
                            subcatcount[subcat.index(cat_2[j])] = subcatcount[subcat.index(cat_2[j])] + 1
                        elif detect(cat_2[j])=="fr":
                            subcat.append(cat_2[j])
                            subcatcount.append(1)
                elif cat_1[i] in subcat:
                    subcatcount[subcat.index(cat_1[i])] = subcatcount[subcat.index(cat_1[i])] + 1 
                elif detect(cat_1[i])=="fr":
                    subcat.append(cat_1[i])
                    subcatcount.append(1)

        return [(subcat[k],subcatcount[k]) for k in range(len(subcat))]
    
    def createandfillcategoriestable(self):

        """Create table <Categories> and fills it with every <subcategories> (every categories provided by OFF for the product)"""

        query = "CREATE TABLE `Categories` ( `id` SMALLINT AUTO_INCREMENT, `subcategorie` VARCHAR({}), `count` SMALLINT, `maincategorie` VARCHAR({}), PRIMARY KEY(`id`))".format(varchar_length,varchar_length)
        cur = self.cnx.cursor()
        cur.execute(query)
        
        for categorie in self.categories:

            categorie = dashtounderscore(categorie)
            datatoinsert = self.listingsubcategories(categorie)

            for data in datatoinsert:
                
                query = "INSERT INTO Categories (subcategorie, count, maincategorie) VALUES (%s,%s,%s)"
                data = [data[0][:varchar_length],data[1],categorie]
                cur = self.cnx.cursor()
                cur.execute(query,data)
                self.cnx.commit()
                cur.close()
    
    def createsubstitutetable(self):
        
        query = "CREATE TABLE `Substitutes` ( `id` SMALLINT, PRIMARY KEY(`id`))"
        cur = self.cnx.cursor()
        cur.execute(query)
        self.cnx.commit()
        cur.close()

    def loaddata(self,data):

        """reinitialize the whole database"""

        self.drop()
        self.connect()
        self.data = data
        self.createglobaltable()
        self.insertdataintoglobaltable()
        self.createandfillcategoriestable()
        self.createsubstitutetable()
    
    def drop(self):

        if self.cnx:
            pass
        else:
            self.connect()
        
        cur = self.cnx.cursor()
        query = "DROP DATABASE {}".format(self.database)
        cur.execute(query)
    
    def insertsubstitute(self,id):

        """Insert the specified id in Substitutes Table"""

        query = "SELECT id FROM Substitutes WHERE id = {}".format(id)
        cur = self.cnx.cursor()
        cur.execute(query)
        pdt = [row for row in cur]
        if not pdt:
            query = "INSERT INTO Substitutes (id) VALUES (%s)"
            cur = self.cnx.cursor()
            cur.execute(query,[id])
            self.cnx.commit()
            cur.close()
        else:
            print("Ce produit fait déjà partie de vos substituts enregistrés")
    
    def getsubstitutes(self):

        """returns a list of dictionnaries, each dictionnary containing every info on the product"""

        query = "SELECT Products.* FROM Substitutes INNER JOIN Products ON Products.id = Substitutes.id"
        cur = self.cnx.cursor(dictionary=True)
        cur.execute(query)
        return [row for row in cur]

    def getproductinfo(self,id):

        """returns a dictionnary containing every info on the product"""

        query = "SELECT {} FROM Products WHERE id = {}".format(self.columnsasstr,id)
        cur = self.cnx.cursor(dictionary=True)
        cur.execute(query)
        return [row for row in cur][0]

    def getcategorielist(self,categorie):

        """returns a list of subcategories name"""
        
        query = "SELECT subcategorie FROM Categories WHERE maincategorie = '{}'".format(dashtounderscore(categorie))
        cur = self.cnx.cursor()
        cur.execute(query)
        return [row[0] for row in cur]
    
    def getlistofproducts(self,categorie,listofsubcategories):

        """returns a list of product id with the said subcategories"""

        query = "SELECT id FROM Products WHERE (categorie = '{}')".format(categorie)
        for subcat in listofsubcategories:
            query = query + "AND (categories REGEXP '.*({}).*')".format(subcat)
        cur = self.cnx.cursor()
        cur.execute(query)
        return [row[0] for row in cur]
    
    def removesub(self,id):

        """removes an id from Substitutes TABLE"""

        query = "DELETE FROM Substitutes WHERE id = {}".format(id)
        cur = self.cnx.cursor()
        cur.execute(query)
        self.cnx.commit()
        cur.close()