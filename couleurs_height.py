from PIL import Image
import numpy as np
import json
from math import sqrt


parametres = json.load(open("parametres.json"))

resolution = parametres["resolution"]
grid_size = parametres["grid_size"]
nb_octaves = parametres["nb_octaves"]
persistence = parametres["persistence"]
height = parametres["height"]

# Hauteurs

h_sea = 0.50
h_sand = 0.53
h_beach = 0.55
h_grass = 0.65
h_forest = 0.75
h_mountain = 0.85

# Couleurs
color = {
    "sea": [65, 105, 225],
    "grass": [34, 139, 34],
    "forest": [0, 100, 0],
    "beach": [238, 214, 175],
    "sand": [210, 180, 140],
    "snow": [255, 250, 250],
    "mountain": [139, 137, 137],
}


image = Image.open("out/image_hauteur.png")

bruit_array = np.array(image).astype(np.float32)

bruit_array = bruit_array / 255.0

couleur = [[[0, 0, 0] for i in range(resolution + 1)] for i in range(resolution + 1)]

for i in range(resolution + 1):
    for j in range(resolution + 1):
        if bruit_array[i][j] < (height + 0.15):
            couleur[i][j] = color["sea"]
        elif bruit_array[i][j] < (height + 0.18):
            couleur[i][j] = color["sand"]
        elif bruit_array[i][j] < (height + 0.20):
            couleur[i][j] = color["beach"]
        elif bruit_array[i][j] < (height + 0.30):
            couleur[i][j] = color["grass"]
        elif bruit_array[i][j] < (height + 0.6):
            couleur[i][j] = color["forest"]
        elif bruit_array[i][j] < (height + 0.8):
            couleur[i][j] = color["mountain"]
        else:
            couleur[i][j] = color["snow"]


couleur_array = np.array(couleur, dtype=np.uint8)

image = Image.fromarray(couleur_array, "RGB")
image.save("out/carte_modified.png")
print("coloré !")
