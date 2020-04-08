from fctions.py import *

print("Outil pour une alimentation plus saine")

while 1:
    choice = input("\n\tVous souhaitez remplacer des aliments tapez 1\n\tVous souhaitez retrouver vos aliments substitués tapez 2\n")
    if choice == "1":
        remplacer_aliments()
    elif choice == "2":
        consulter_substituts()
    else:
        print("Merci de suivre les instructions qui s'affichent dans le terminal")