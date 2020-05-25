import time
from parameters import CHOSENGRADES, VARCHARLENGHT, CHOSENCOLUMNS, N
from dialogwithoffapi.openfoodrequest import Openfoodrequest


class Extractfromrequest():

    """class extracting the data from an API Response
    to  a one-categorie-request"""

    def __init__(self, name):
        self.name = name
        self.data = []

    def get(self):

        """fills self.data with categories data
        self.data is a list of dictionnaries
        returns self.data"""

        compting = 0

        for grade in CHOSENGRADES:

            print("Importing data :\t"+self.name+" "+grade, end="\n\t\t\t\t\t")
            apiresponse = Openfoodrequest(self.name, grade, N).get()
            before = time.time()
            rawdata = apiresponse

            for idproduct in range(min(N, int(rawdata["count"]))):

                self.data.append({})

                for column in CHOSENCOLUMNS:
                    # since no fields are sure to exist except for bar_code
                    # we have to anticipate KeyError
                    try:
                        if column == "categorie":
                            self.data[compting][column] = self.name
                        else:
                            self.data[compting][column] = (
                                rawdata["products"][idproduct]
                                [column][:VARCHARLENGHT]
                            )
                    except KeyError:
                        self.data[idproduct][column] = ""
            # waiting 1 second between each API Request
            after = time.time()

            while after-before < 1:

                after = time.time()

            print("Done")
        return self.data
