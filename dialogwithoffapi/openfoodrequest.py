import requests
from parameters import N, CHOSENCOLUMNS


class Openfoodrequest():

    """Class representing the specific type
    of request to openfooddata our App will use"""

    def __init__(self, categorie, grade):

        """creating the url so we ask for N products
        from <categorie> with nutrition <grade> in .json"""

        self.url1 = (
            "https://fr.openfoodfacts.org"
            "/cgi/search.pl?action=process&"
            "tagtype_0=categories&tag_contains_0=contains&tag_0="
        )
        self.url2 = (
            "&tagtype_1=nutrition_grade_fr&"
            "tag_contains_1=contains&tag_1="
        )
        self.url3 = "&page_size="+str(N)+"&json=True"
        self.url4 = "&fields="
        for i in CHOSENCOLUMNS:
            if i == "categorie":
                continue
            else:
                self.url4 = self.url4+i+","
        self.url4 = self.url4[:-1]
        self.url = (
            self.url1 + str(categorie)
            + self.url2 + str(grade)
            + self.url3
            + self.url4
        )
        self.headers = {
            'User-Agent': 'OpenclassroomP5 - Unix - Version 2'
        }
        self.payload = {}

    def get(self):

        """Sending the get request to openfoodfact API
        returns a json file
        raises ValueError if request fails"""

        self.apiresponse = requests.request(
            "GET", self.url, headers=self.headers,
            data=self.payload
        )

        if self.apiresponse.ok:

            return self.apiresponse.json()

        else:

            raise ValueError
