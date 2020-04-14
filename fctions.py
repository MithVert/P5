import mysql.connector

def connect_to_mysql():
    cnx = mysql.connector.connect(user='gery', password='Khan54Me215', host='localhost', database='')
    return cnx

def log_out():
    return cnx.close()