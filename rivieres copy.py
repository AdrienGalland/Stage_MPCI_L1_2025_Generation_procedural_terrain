from PIL import Image
import numpy as np
import json


def rivieres(x, y, grille, liste_riviere=None):
    if liste_riviere == None:
        liste_riviere = [(x, y)]
    if grille[y][x] < 0.15:
        return liste_riviere
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
    # minimum = (cases_inspectees_x[0], cases_inspectees_y[0])
    # for i in cases_inspectees_x:
    #     for j in cases_inspectees_y:
    #         if grille[j][i] < grille[minimum[1]][minimum[0]] and (i, j) not in liste_riviere:
    #             minimum = (i, j)
    # liste_riviere.append(minimum)
    # return rivieres(minimum[0], minimum[1], grille, liste_riviere)

    liste_cases = []
    for i in cases_inspectees_x:
        for j in cases_inspectees_y:
            liste_cases.append((i, j))

    liste_cases.sort(key=lambda case: grille[case[1]][case[0]])
    print(liste_cases)
    for case in liste_cases:
        if case not in liste_riviere and grille[case[1]][case[0]] < grille[y][x]:
            liste_riviere.append(case)
            liste_embranchement = rivieres(case[0], case[1], grille, liste_riviere)
            for case2 in liste_embranchement:
                liste_riviere.append(case2)
    return liste_riviere


image_gris = Image.open("out/image_gradient.png")

bruit_array = np.array(image_gris).astype(np.float32)

bruit_array = bruit_array / 255.0

liste_rivieres = rivieres(500, 500, bruit_array)

liste_rivieres += rivieres(500, 540, bruit_array)
liste_rivieres += rivieres(420, 556, bruit_array)

couleur = Image.open("out/carte.png").convert("RGB")
couleur_array = np.array(couleur)

for case in liste_rivieres:
    couleur_array[case[1]][case[0]] = [0, 180, 255]

image = Image.fromarray(couleur_array, "RGB")
image.save("out/carte_rivieres.png")
