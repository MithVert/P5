# "Pur Beurre"'s App to find healthier food

This app aim at helping people find healthier products.
It imports its data from OpenFoodFact which is mostly referred to as OFF in the
code.

## Getting Started

Clone or fork the repository.

### Prerequisites

See requirements.txt for every python lib you need.
You'll need to install python3 beforehand if you don't have it already.


```
You can install python this way :

Linux:
type in command line :
sudo apt-get install python3

For other systems download and install the corresponding package from :
https://www.python.org/downloads/


To install every library listed in requirements.txt

you can use pip in command line:
pip3 install <library>

You can check the library already installed in your environment
with this command:
pip3 freeze
```

You also need to install MySQL before running the app and make sure to have a
credentials.json file containing in a dictionnary :
"host" : "openfooddatahost"
"user" : "username"
"password" : "userpassword"
Where the user has privileges on openfooddata.* in MySQL
I you want, to can use a different databasename than openfooddata.
To do so make sure to change DATABASENAME in parameters.py

### Running

Run main.py with python3 and then follow the instructions the app will give you.
You may modify parameters.py beforehand while following the instructions given
in comments if you want to adjust the app to your needs.
At launch the app will ask wether you want to restart from scratch and reload
every data. It is advised not to do so unless you run it for the first time.

```
For instance through command line:
python3 main.py
```

Make sure you launch the app from its root which is the "P5" folder

## Contributing

As this is a project which is part of my studies,
I don't allow external contributions for now.

## Authors

* **Géry Boulangé** - *Initial work* - [MithVert](https://github.com/MithVert)

## Acknowledgments

* To my mentor Rygel Louv who kept helping me out
* To Thierry Chappuis whose webinars and answers were of great use
* To Seb Declercq whose explanations were appreciated
