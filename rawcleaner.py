#! /usr/bin/env python3
# coding: utf-8

import json

class Datafile():

    def __init__(self,file):

        rawfile = open(file,"r")
        self.rawdata = json.load(rawfile)
        self.title = rawfile.name[6:-5]
        rawfile.close()
        self.columns = ["product_name","generic_name","nutrition_grade_fr","stores","url"]
        self.fine = ""
        
    
    def __repr__(self):

        if self.fine == "":
            return self.title
        else:
            return self.fine

    def getraw(self):

        return self.rawdata
    
    def createfine(self):

        for column in self.columns:
            if column == "url":
                self.fine = self.fine + column + "\n"
            else:
                self.fine = self.fine + column + ";"
        
        for idproduct in range(self.rawdata["count"]):
            for column in self.columns:
                print(self.fine)
                if column == "url":
                    self.fine = self.fine + self.rawdata["products"][idproduct][column] + "\n"
                else:
                    self.fine = self.fine + self.rawdata["products"][idproduct][column] + ";"
    
    def getfine(self):

        return self.fine

    def save_as_csv(self, file="default"):

        if file == "default":
            file = self.title + ".csv"
        
        csvfile = open(file, "w")
        csvfile.write(self.fine)
        csvfile.close()

if __name__ == "__main__":

    """just for testing the class"""
    biscuits_et_gateauxgradea = Datafile("bddrawbiscuits-et-gateauxgradea.json")
    print(biscuits_et_gateauxgradea)
    biscuits_et_gateauxgradea.createfine()
    print(biscuits_et_gateauxgradea)
    biscuits_et_gateauxgradea.save_as_csv()

#every field is optionnal, got to test wether it exists before trying to get its value