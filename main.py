#! /usr/bin/env python3
# coding: utf-8

from parameters import *
from dialogwithMySQL import *
from dialogwithOFFAPI import *

if __name__=="__main__":
    data = []
    for categorie in chosencategories:
        a = Categorie(categorie).get()
        data = data + a
    sqlcreator = Sqldatabase(data)
    sqlcreator.createglobaltable()
    sqlcreator.insertdataintoglobaltable()
    sqlcreator.createcategorietables()