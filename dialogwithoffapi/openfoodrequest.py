import requests
from parameters import N, CHOSENCOLUMNS


class Openfoodrequest():

    """Class representing the specific type
    of request to openfooddata our App will use"""

    def __init__(self, categorie, grade):

        """creating the url so we ask for N products
        from <categorie> with nutrition <grade> in .json"""

        url1 = (
            "https://fr.openfoodfacts.org"
            "/cgi/search.pl?action=process&"
            "tagtype_0=categories&tag_contains_0=contains&tag_0="
        )
        url2 = (
            "&tagtype_1=nutrition_grade_fr&"
            "tag_contains_1=contains&tag_1="
        )
        url3 = "&page_size="+str(N)+"&json=True"
        url4 = "&fields="
        for i in CHOSENCOLUMNS:
            if i == "categorie":
                continue
            else:
                url4 = url4+i+","
        url4 = url4[:-1]
        self.url = (
            url1 + str(categorie)
            + url2 + str(grade)
            + url3
            + url4
        )
        self.headers = {
            'User-Agent': 'OpenclassroomP5 - Unix - Version 2'
        }
        self.payload = {}
        self.categorie = categorie

    def get(self):

        """Sending the get request to openfoodfact API
        returns a json file
        raises ValueError if request fails"""

        apiresponse = requests.request(
            "GET", self.url, headers=self.headers,
            data=self.payload
        )

        if apiresponse.ok:

            returneddata = apiresponse.json()["products"]

            for productdata in returneddata:

                productdata["maincategorie"] = self.categorie

            return returneddata

        else:

            raise ValueError
