from database.sqldatabasemanager import Sqldatabasemanager
from view.interfaceclient import Interfaceclient


def main():

    sqlmng = Sqldatabasemanager()
    interface = Interfaceclient(sqlmng)
    interface.welcome()


if __name__ == "__main__":
    main()
