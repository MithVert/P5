"""a few utility fonctions"""


def dashtounderscore(string):
    string_temp = ""
    for i in string:
        if i == "-":
            string_temp = string_temp + "_"
        else:
            string_temp = string_temp + i
    return string_temp


def underscoretodash(string):
    string_temp = ""
    for i in string:
        if i == "_":
            string_temp = string_temp + "-"
        else:
            string_temp = string_temp + i
    return string_temp
