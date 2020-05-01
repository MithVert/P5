import mysql.connector
import json
from parameters import *
from langdetect import detect, DetectorFactory
from dialogwithOFFAPI import *
from utilityfonctions import *
DetectorFactory.seed = 0

class Sqldatabase():

    """Class used to dialog with MySQL local database"""

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

        subcategories = []
        subcategoriescount = []

        cur = self.cnx.cursor()
        query = """SELECT categories FROM produits WHERE categorie = "{}" ;""".format(underscoretodash(categorie))
        cur.execute(query)

        for categories in cur:
            
            categories_temp = categories[0].split(", ")

            for i in range(len(categories_temp)):
                if ":" in categories_temp[i]:
                    continue
                elif "," in categories_temp[i]:
                    categories_temp_2 = categories_temp[i].split(",")
                    for j in range(len(categories_temp_2)):
                        if categories_temp_2[j] in subcategories:
                            subcategoriescount[subcategories.index(categories_temp_2[j])] = subcategoriescount[subcategories.index(categories_temp_2[j])] + 1
                        elif detect(categories_temp_2[j])=="fr":
                            subcategories.append(categories_temp_2[j])
                            subcategoriescount.append(1)
                elif categories_temp[i] in subcategories:
                    subcategoriescount[subcategories.index(categories_temp[i])] = subcategoriescount[subcategories.index(categories_temp[i])] + 1 
                elif detect(categories_temp[i])=="fr":
                    subcategories.append(categories_temp[i])
                    subcategoriescount.append(1)
        
        return [(subcategories[k],subcategoriescount[k]) for k in range(len(subcategories))]
    
    def createandfillcategoriestable(self):

        """Create table `Categories` for each categorie in chosencategories - Fills them with every OFFCategorie among the products from the categorie"""

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
        
        table = "CREATE TABLE `Substitutes` ( `id` SMALLINT, PRIMARY KEY(`id`))".format(varchar_length)
        cur = self.cnx.cursor()
        cur.execute(table)
        self.cnx.commit()
        cur.close()

    def loaddata(self,data):

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
        if pdt == []:
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
        
        query = "SELECT {} FROM Table_{}".format(dashtounderscore(categorie),dashtounderscore(categorie))
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
