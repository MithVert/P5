"""A few functions used for interfacing"""


def errmessage():
    print("Merci de n'utiliser que les commandes précisées entre crochets")


def choice(listofoptions):
    while True:
        for i in range(len(listofoptions)):
            print("\t[{}] {} ".format(i, listofoptions[i]))
        userchoice = input("Votre choix: ")
        try:
            userchoice = int(userchoice)
            if userchoice in range(len(listofoptions)):
                return userchoice, listofoptions[userchoice]
            else:
                errmessage()
        except ValueError:
            errmessage()
