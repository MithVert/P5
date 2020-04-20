#! /usr/bin/env python3
# coding: utf-8

"""to be deleted"""

import json

class JSONDatafile():

    """class including every method we need to retrieve what we wants from the jsonfile the openfoodfact API gave us"""

    def __init__(self,file):

        rawfile = open(file,"r")
        self.rawdata = json.load(rawfile)
        self.title = rawfile.name[6:-5]
        rawfile.close()
        self.columns = ["product_name","generic_name","nutrition_grade_fr","stores","url"]
        self.fine = ""
        
    
    def __repr__(self):

        """This method only has testing purposes"""

        if self.fine == "":
            return self.title
        else:
            return self.fine
    
    def createfine(self):

        """fills self.fine with the data we fetch from the api json file, returns a string csv-formated"""

        for column in self.columns:
            if column == "url":
                self.fine = self.fine + column + "\n"
            else:
                self.fine = self.fine + column + ";"
        
        for idproduct in range(min(50,self.rawdata["count"])):
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

    def save_as_csv(self, file="default"):

        """save the extracted data as a csv file"""

        if file == "default":
            file = self.title + ".csv"
        
        if self.fine == "":
            self.createfine()
        
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
        data = JSONDatafile(i)
        data.save_as_csv()
        print("Done")