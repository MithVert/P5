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
        
        for idproduct in range(50):
            for column in self.columns:
                #since no fields are sure to exist except for bar_code, we have to anticipate KeyError
                try:
                    if column == "url":
                        self.fine = self.fine + self.rawdata["products"][idproduct][column] + "\n"
                    else:
                        self.fine = self.fine + self.rawdata["products"][idproduct][column] + ";"
                except KeyError:
                    if column == "url":
                        self.fine = self.fine + "\n"
                    else:
                        self.fine = self.fine + ";"
    
    def getfine(self):

        return self.fine

    def save_as_csv(self, file="default"):

        if file == "default":
            file = self.title + ".csv"
        
        csvfile = open(file, "w")
        csvfile.write(self.fine)
        csvfile.close()

if __name__ == "__main__":
    print("initialisation")
    chosen_data = ("boissons","plats-prepares","biscuits-et-gateaux","produits-a-tartiner-sucres","sauces")
    chosen_data_file = []
    for i in chosen_data:
        for j in ("gradea","gradeb"):
            chosen_data_file.append("bddraw"+i+j+".json")
    
    for i in chosen_data_file:
        print(i, end="\t\t")
        data = Datafile(i)
        data.createfine()
        data.save_as_csv()
        print("Done")