#! /usr/bin/env python3
# coding: utf-8

import requests

import time

import json

class   OpenfoodRequest():

    """Class representing the specific type of request to openfooddata our App will use"""

    def __init__(self,categorie,grade):

        """creating the url so we ask for 50 products from <categorie> with nutrition grade <grade> in .json"""

        self.url1 = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0="
        self.url2 = "&tagtype_1=nutrition_grade_fr&tag_contains_1=contains&tag_1="
        self.url3 = "&page_size=50&json=True"
        self.url = self.url1 + str(categorie) + self.url2 + str(grade) + self.url3
        self.headers = {
            'User-Agent':'OpenclassroomP5 - Unix - Version 2'
        }
        self.payload = {}

    def get(self):

        """Sending the get request to openfoodfact API - returns a json file"""

        self.apiresponse = requests.request("GET", self.url, headers=self.headers, data=self.payload)

        if self.apiresponse.ok:

            return self.apiresponse.json()

        else:

            raise ValueError

def creating_raw_file(chosen_categories = ("boissons","plats-prepares","biscuits-et-gateaux","produits-a-tartiner-sucres","sauces"),chosen_grades = ("a","b")):

    """Uses Openfoodrequest class - create separates json files for every chosen categories and grades"""

    for categorie in chosen_categories:

        for grade in chosen_grades:

            print("Importing data :\t"+categorie+" "+grade,end="\n\t\t\t\t\t")
            raw_file = open("bddraw"+categorie+"grade"+grade+".json","w",encoding="utf-8")
            api_response_json = OpenfoodRequest(categorie, grade).get()
            before = time.time()
            json.dump(api_response_json, raw_file)
            raw_file.close()
            after = time.time()
            #waiting 1 second between each API Request
            while after-before < 1:
                after = time.time()
            print("Done")

if __name__=="__main__":
    creating_raw_file()