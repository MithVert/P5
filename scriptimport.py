#! /usr/bin/env python3
# coding: utf-8

import requests

import time

import json as jsmodule


class   OpenfoodRequest():

    """Class representing the specific type of request to openfooddata our App will use"""

    def __init__(self, data, page=1):
        self.openurl = "https://fr.openfoodfacts.org/categorie/"
        self.page = "&page="
        self.json = ".json"
        self.headers = {
            'User-Agent':'OpenclassroomP5 - Unix - Version 1.0'
        }
        self.payload = {}
        self.url = self.openurl+data+self.page+str(page)+self.json
    
    def get(self):
        self.apiresponse = requests.request("GET", self.url, headers=self.headers, data=self.payload)
        if self.apiresponse.ok:
            return self.apiresponse.json()
        else:
            raise ValueError

def creating_raw_file():

    """Script importing data as JSON file from openfoodfacts API"""

    chosen_data = ("boissons","plats-prepares","biscuits-et-gateaux","produits-a-tartiner-sucres","sauces")
    for data in chosen_data:
        print("Importing data :", data)
        for i in range(5):
            before = time.time()
            raw_data_file = open("bddraw"+data+"page"+str(i+1)+".json","w",encoding="utf-8")
            api_response_json = OpenfoodRequest(data, page=i+1).get()
            jsmodule.dump(api_response_json, raw_data_file)
            raw_data_file.close()
            after = time.time()
            while after-before < 1:
                after = time.time()
        print("\t\t\t\t\tDone")

if __name__=="__main__":
    creating_raw_file()