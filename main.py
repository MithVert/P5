#! /usr/bin/env python3
# coding: utf-8

from parameters import *
from dialogwithMySQL import *
from dialogwithOFFAPI import *

if __name__=="__main__":
    data = []
    #for categorie in chosencategories:
    #    data = data + Categorie(categorie).get()
    sqlcreator = Sqldatabasecreator(data)
    #sqlcreator.connect()
    #sqlcreator.createtable()
    #sqlcreator.insertdataintotable()
    sqlcreator.createcategorietables()