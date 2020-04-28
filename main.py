#! /usr/bin/env python3
# coding: utf-8

from parameters import *
from dialogwithMySQL import *
from dialogwithOFFAPI import *
from interface import *

if __name__=="__main__":

    while True:

        print("Bienvenue sur notre application pour manger plus saînement")
        print("Souhaitez-vous")
        userchoice = choice(["Réinitialiser les Bases de Données", "Continuer avec les données enregistrées", "Quitter"])

        if userchoice[0] == 0:
            sqldatabase = Sqldatabase()
            sqldatabase.loaddata(getalldata())
        
        elif userchoice[0] == 1:
            sqldatabase = Sqldatabase()
        
        elif userchoice[1] == "Quitter":
            break