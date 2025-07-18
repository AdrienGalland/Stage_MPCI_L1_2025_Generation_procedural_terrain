from PIL import Image
import numpy as np
import json
import random
import sys
from random import randint

sys.setrecursionlimit(30000)


def add_rivers_infiltration(x, y, grille):

    def rivieres(x, y, grille, liste_riviere=None) -> list:
        if grille[y][x] < 0.15:
            return liste_riviere
        if liste_riviere is None:
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

        liste_cases.sort(key=lambda case: grille[case[1]][case[0]])  # Trie les cases par altitude croissante
        print(liste_cases)

        for case in liste_cases:
            if case not in liste_riviere:
                liste_riviere.append(case)
                return rivieres(case[0], case[1], grille, liste_riviere)
        return liste_riviere

    return rivieres(x, y, grille)

    # image_gris = Image.open("out/image_gradient.png")

    # bruit_array = np.array(image_gris).astype(np.float32)

    # bruit_array = bruit_array / 255.0

    # liste_rivieres = rivieres(x, y, bruit_array)

    # couleur = Image.open("out/carte.png").convert("RGB")
    # couleur_array = np.array(couleur)

    # for case in liste_rivieres:
    #     couleur_array[case[1]][case[0]] = [0, 180, 255]

    # image = Image.fromarray(couleur_array, "RGB")
    # image.save("out/carte_modified.png")
