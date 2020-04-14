#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
import json

class Produits():
    
    def __init__(categorie):


list_nutrition_grade = []
for i in range(1,6):
    #parcours des fichiers d'une même catégorie -> donnera une même table
    file = "bddrawbiscuits-et-gateauxpage"+str(i)+".json"
    for j in range(20):
        #parcours des vingts produits contenus dans chaque page
        list_nutrition_grade.append(json.load(open(file,"r"))["products"][j]["nutrition_grade_fr"])

for i in ("a","b","c","d","e"):
    print(i+":",list_nutrition_grade.count(i))

#https://documenter.getpostman.com/view/8470508/SVtN3Wzy?version=latest#f564abb6-b306-4f8c-aa32-80c37f3d7fca