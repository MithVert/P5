#! /usr/bin/env python3
# coding: utf-8

import requests
import time
import json

chosencategories = ("boissons","plats-prepares","biscuits-et-gateaux","produits-a-tartiner-sucres","sauces")

class   OpenfoodRequest():

    """Class representing the specific type of request to openfooddata our App will use"""

    def __init__(self,categorie,grade,n):

        """creating the url so we ask for <n> products from <categorie> with nutrition <grade> in .json"""

        self.url1 = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0="
        self.url2 = "&tagtype_1=nutrition_grade_fr&tag_contains_1=contains&tag_1="
        self.url3 = "&page_size="+str(n)+"&json=True"
        self.url = self.url1 + str(categorie) + self.url2 + str(grade) + self.url3
        self.headers = {
            'User-Agent':'OpenclassroomP5 - Unix - Version 2'
        }
        self.payload = {}

    def get(self):

        """Sending the get request to openfoodfact API - returns a json file - raises value Error if request fails"""

        self.apiresponse = requests.request("GET", self.url, headers=self.headers, data=self.payload)

        if self.apiresponse.ok:

            return self.apiresponse.json()

        else:

            raise ValueError

class Categorie():

    """class getting and storing the data corresponding to one categorie"""

    def __init__(self, name, n=50, grades=("a","b"), columns=["product_name","generic_name","nutrition_grade_fr","stores","url"]):

        self.name = name
        self.chosengrades = grades
        self.columns = columns
        self.n = n
        self.data = []
    
    def get(self):

        """fills self.data with categories' data, data is a list of dictionnary"""

        for grade in self.chosengrades:

            print("Importing data :\t"+self.name+" "+grade,end="\n\t\t\t\t\t")
            apiresponse = OpenfoodRequest(self.name, grade, self.n).get()
            before = time.time()
            rawdata = json.loads(apiresponse)

            for idproduct in range (min(self.n,rawdata["count"])):

                for column in self.columns:

                    self.data.append({})
                    #since no fields are sure to exist except for bar_code, we have to anticipate KeyError
                    try:
                        self.data[idproduct][column] = rawdata["products"][idproduct][column]
                    except KeyError:
                        self.data[idproduct][column] = ""

            #waiting 1 second between each API Request
            after = time.time()

            while after-before < 1:

                after = time.time()

            print("Done")
    
    def savetomysql(self):

        if self.data == []:
            self.get()