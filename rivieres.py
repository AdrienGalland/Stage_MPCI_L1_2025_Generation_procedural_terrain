from PIL import Image
import numpy as np
import json
import random
import sys
from random import shuffle
from couleurs import couleurs

sys.setrecursionlimit(30000)


def add_rivers(x, y, grille, coefficient) -> list:
    print("départ", (x, y))

    def rivieres(x, y, grille, coefficient, liste_riviere=[]):
        if grille[y][x] < 0.15 / coefficient:
            return liste_riviere
        if liste_riviere is []:
            liste_riviere = [(x, y)]
        cases_inspectees_x = [x]
        cases_inspectees_y = [y]
        if x != 0:
            cases_inspectees_x.append(x - 1)
        if x < len(grille[0]) - 1:
            cases_inspectees_x.append(x + 1)
        if y != 0:
            cases_inspectees_y.append(y - 1)
        if y < len(grille) - 1:
            cases_inspectees_y.append(y + 1)

        liste_cases = []
        for i in cases_inspectees_x:
            for j in cases_inspectees_y:
                if (i, j) != (x, y):
                    liste_cases.append((i, j))
        # shuffle(liste_cases)
        liste_cases.sort(key=lambda case: grille[case[1]][case[0]])
        print(liste_cases)

        for case in liste_cases:
            if case not in liste_riviere:
                liste_riviere.append(case)
                print(case[0], case[1])
                return rivieres(case[0], case[1], grille, coefficient, liste_riviere)
        case_invalide = liste_riviere.pop(-1)
        liste_riviere = [case_invalide] + liste_riviere
        print(liste_riviere)
        print(liste_riviere[-1][0], liste_riviere[-1][1])
        return rivieres(
            liste_riviere[-1][0], liste_riviere[-1][1], grille, coefficient, liste_riviere
        )

    return rivieres(x, y, grille, coefficient)


    # couleur = Image.open("out/carte.png").convert("RGB")
    # couleur_array = np.array(couleur)

    # for case in liste_rivieres:
    #     couleur_array[case[1]][case[0]] = [0, 180, 255]

    # image = Image.fromarray(couleur_array, "RGB")
    # image.save("out/carte_modified.png")
    print("généré")
