from PIL import Image
import numpy as np
import json
from math import sqrt


def image_gradient():

    # Paramètres

    parametres = json.load(open("parametres.json"))

    resolution = parametres["resolution"]
    grid_size = parametres["grid_size"]
    nb_octaves = parametres["nb_octaves"]
    persistence = parametres["persistence"]
    height_multiplicator = parametres["height_multiplicator"]
    percent_water = parametres["percent_water"]

    def smoothstep(x):
        return 6 * (x**5) - 15 * (x**4) + 10 * (x**3)

    # Génération du gradient circulaire

    center_x, center_y = resolution // 2, resolution // 2

    circle_grad = [[0.0 for i in range(resolution + 1)] for i in range(resolution + 1)]

    for j in range(resolution + 1):
        for i in range(resolution + 1):
            dist_x = abs(i - center_x)
            dist_y = abs(j - center_y)
            dist = sqrt(dist_x**2 + dist_y**2)
            circle_grad[i][j] = -dist * percent_water

    # get it between -1 and 1
    # max_grad = np.max(circle_grad)
    # circle_grad = circle_grad / max_grad
    # circle_grad -= 0.5
    # circle_grad *= 2.0
    # circle_grad = -circle_grad

    # shrink gradient
    # for y in range(resolution + 1):
    #     for x in range(resolution + 1):
    #         if circle_grad[y][x] > 0:
    #             circle_grad[y][x] *= 20

    # get it between 0 and 1
    circle_grad = (circle_grad - np.min(circle_grad)) / (
        np.max(circle_grad) - np.min(circle_grad)
    )


    # circle2 = circle_grad * 255
    # circle2 = circle2.astype(np.uint8)

    # image_circle = Image.fromarray(circle2, mode='L')
    # image_circle.show()

    f = open("out/grayscale.json", "r")

    bruit_array = np.array(json.load(f), dtype=np.float32)

    # print(np.max(bruit_array), np.min(bruit_array))

    for j in range(resolution + 1):
        for i in range(resolution + 1):
            x = i / resolution
            y = j / resolution
            bruit_array[i][j] *= smoothstep(circle_grad[i][j]) * height_multiplicator

    # print(np.max(bruit_array), np.min(bruit_array))

    # bruit_array = np.clip(bruit_array, 0, 1)

    coefficient = np.max(bruit_array)

    bruit_array = bruit_array / np.max(bruit_array)

    gray_level = (bruit_array * 255).astype(np.uint8)

    # gray_level.clip(0, 255)

    image_finale = Image.fromarray(gray_level, mode="L")

    image_finale.save("out/image_gradient.png")

    return coefficient
