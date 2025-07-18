# from PIL import Image
import numpy as np
from math import sqrt


def terraforming(x, y, rayon, height, grille, plane=False):
    def smoothstep(x):
        return 6 * (x**5) - 15 * (x**4) + 10 * (x**3)

    def modify_height(tableau, center_x, center_y, rayon, height, plane=False):
        liste_pixel = []
        if not plane:
            for x in range(
                int(max(center_x - rayon, 0)),
                int(min(center_x + rayon, len(tableau[0]))),
            ):
                for y in range(
                    int(max(center_y - rayon, 0)),
                    int(min(center_y + rayon, len(tableau))),
                ):
                    dx = x - center_x
                    dy = y - center_y
                    distance = sqrt(dx**2 + dy**2)
                    if distance <= rayon:
                        height_increase = smoothstep(1 - (distance / rayon)) * height
                        tableau[y][x] += height_increase
        else:
            liste_coordonnees = []
            for x in range(
                int(max(center_x - rayon, 0)),
                int(min(center_x + rayon, len(tableau[0]))),
            ):
                for y in range(
                    int(max(center_y - rayon, 0)),
                    int(min(center_y + rayon, len(tableau))),
                ):
                    dx = x - center_x
                    dy = y - center_y
                    distance = sqrt(dx**2 + dy**2)
                    if distance <= 0.8 * rayon:
                        liste_pixel.append(tableau[y][x])
                        liste_coordonnees.append((x, y))
            moyenne = sum(liste_pixel) / len(liste_pixel)

            for coordonnées in liste_coordonnees:
                if tableau[coordonnées[1]][coordonnées[0]] < moyenne and moyenne - tableau[coordonnées[1]][coordonnées[0]] >= height:
                    tableau[coordonnées[1]][coordonnées[0]] += height
                elif tableau[coordonnées[1]][coordonnées[0]] < moyenne and moyenne - tableau[coordonnées[1]][coordonnées[0]] < height:
                    tableau[coordonnées[1]][coordonnées[0]] = moyenne
                elif tableau[coordonnées[1]][coordonnées[0]] > moyenne and tableau[coordonnées[1]][coordonnées[0]] - moyenne >= height:
                    tableau[coordonnées[1]][coordonnées[0]] -= height
                elif tableau[coordonnées[1]][coordonnées[0]] > moyenne and tableau[coordonnées[1]][coordonnées[0]] - moyenne < height:
                    tableau[coordonnées[1]][coordonnées[0]] = moyenne

    modify_height(grille, x, y, rayon, height, plane)

    np.clip(grille, 0, 1)

    return grille

    # image_finale = Image.fromarray(grille.astype(np.uint8), mode="L")

    # image_finale.save("out/image_hauteur.png")


# image_gris = Image.open("out/image_gradient.png")

# bruit_array = np.array(image_gris).astype(np.float32)

# bruit_array /= 255

# terraforming(500, 500, 100, -0.5, bruit_array)
