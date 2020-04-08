#! /usr/bin/env python3
# coding: utf-8

import requests

def main():
    jsonfiles = []
    collections = ("boissons.json","plats-prepares.json","biscuits-et-gateaux.json","produits-a-tartiner-sucres.json","sauces.json")
    query = "https://fr.openfoodfacts.org/categories/"
    for i in collections:
        jsonfiles.append(requests.get(query+i))
    



if __name__=="__main__":
    main()
