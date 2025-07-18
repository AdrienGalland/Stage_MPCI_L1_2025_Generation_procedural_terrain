import matplotlib.pyplot as plt
import numpy as np
from random import randint, random
from math import ceil, floor, sqrt
from PIL import Image
import json

def matrice_bruit_perlin():
    def smoothstep(x):
        return 6 * (x**5) - 15 * (x**4) + 10 * (x**3)


    def lerp(low, sup, fraction):  # linear interpolation
        return low + fraction * (sup - low)


    def generate_grid(size):
        grid = []
        for i in range(size + 1):
            line = []
            for j in range(size + 1):
                angle = random() * 2 * np.pi
                line.append((np.cos(angle), np.sin(angle)))  # vecteur unitaire aléatoire
            grid.append(line)
        return grid


    def perlin_noise(x, y, grille):  # Bilinear interpolation
        x0 = floor(x)
        x1 = ceil(x)
        y0 = floor(y)
        y1 = ceil(y)

        fonction_x = smoothstep(x - x0)
        fonction_y = smoothstep(y - y0)

        dot_bottom_left = np.dot((x - x0, y - y0), grille[y0][x0])
        dot_bottom_right = np.dot((x - x1, y - y0), grille[y0][x1])
        dot_top_left = np.dot((x - x0, y - y1), grille[y1][x0])
        dot_top_right = np.dot((x - x1, y - y1), grille[y1][x1])

        lerp_bottom = lerp(dot_bottom_left, dot_bottom_right, fonction_x)
        lerp_top = lerp(dot_top_left, dot_top_right, fonction_x)

        value = lerp(lerp_bottom, lerp_top, fonction_y)

        return value


    # Paramètres

    f = open("out/grayscale.json", "w")

    parametres = json.load(open("parametres.json"))

    resolution = parametres["resolution"]
    grid_size = parametres["grid_size"]
    nb_octaves = parametres["nb_octaves"]
    persistence = parametres["persistence"]


    bruit = [[0 for i in range(resolution + 1)] for i in range(resolution + 1)]

    for k in range(nb_octaves):
        grille = generate_grid(grid_size * 2**k)
        for j in range(resolution + 1):
            ligne = []
            for i in range(resolution + 1):
                x = i / (resolution / (grid_size * 2**k))
                y = j / (resolution / (grid_size * 2**k))
                bruit[i][j] += perlin_noise(x, y, grille) * (persistence**k)


    bruit_array = np.array(bruit, dtype=np.float32)

    bruit_array = (bruit_array - np.min(bruit_array)) / (
        np.max(bruit_array) - np.min(bruit_array)
    )

    json.dump(bruit_array.tolist(), f)


# plt.imshow(bruit_array, cmap="gray", interpolation="nearest")
# plt.title("Bruit de Perlin")
# plt.colorbar()
# plt.show()
