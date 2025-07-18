import pyglet
import json
from rivieres import add_rivers
from height import terraforming
import numpy as np
from PIL import Image
from couleurs import couleurs
from matrice_bruit_perlin import matrice_bruit_perlin
from image_gradient import image_gradient
from rivieres_infiltration import add_rivers_infiltration

parametres = json.load(open("parametres.json"))

resolution_map = parametres["resolution"]
grid_size = parametres["grid_size"]
nb_octaves = parametres["nb_octaves"]
persistence = parametres["persistence"]
height = parametres["height"]

resolution = 1000

riviere_infiltration = False


class MapGenerator(pyglet.window.Window):
    def __init__(self):
        super().__init__(fullscreen=True, resizable=True)

        self.icone_riviere = pyglet.image.load("icone_riviere.png")
        self.icone_riviere_clique = pyglet.image.load("icone_riviere_clique.png")
        self.icone_terraforming = pyglet.image.load("icone_terraforming.png")
        self.icone_terrfaforming_clique = pyglet.image.load(
            "icone_terraforming_clique.png"
        )

        self.fenetre = 1

        self.coefficient = 1

        self.explication_riviere = pyglet.text.Label(
            "Cliquez à un endroit sur la carte pour placer une source. La rivière peut être assez longue à générer si elle a beaucoup de chemin à parcourir.\n\nIl est de plus recommandé de terraformer la carte avant de placer les rivières, car chaque chaque terraformation nécessitera de recalculer le parcours des rivières.",
            x=resolution + 3 * (self.width - resolution) // 4,
            y=self.height // 2,
            multiline=True,
            width=0.8 * (self.width - resolution) // 2,
            color=[0, 0, 0],
            align="center",
            anchor_x="center",
            anchor_y="center",
            font_size=15,
        )

        self.explication_terraforming = pyglet.text.Label(
            "Rabaissez le terrain en cliquant avec le bouton gauche de la souris, relevez le terrain avec le bouton droit et aplanissez-le avec un clic molette.\n\n Augmentez ou dimunuez la taille de l'outil avec la molette de la souris.",
            x=resolution + 3 * (self.width - resolution) // 4,
            y=self.height // 2,
            multiline=True,
            width=0.8 * (self.width - resolution) // 2,
            color=[0, 0, 0],
            align="center",
            anchor_x="center",
            anchor_y="center",
            font_size=15,
        )

        self.explication_base = pyglet.text.Label(
            "Sélectionnez un des outils ci-dessus pour modifier la carte générée",
            x=resolution + 3 * (self.width - resolution) // 4,
            y=self.height // 2,
            multiline=True,
            width=0.8 * (self.width - resolution) // 2,
            color=[0, 0, 0],
            align="center",
            anchor_x="center",
            anchor_y="center",
            font_size=15,
        )

        self.explication_border = pyglet.shapes.BorderedRectangle(
            x=resolution + 3 * (self.width - resolution) // 4,
            y=self.height // 2,
            width=0.9 * (self.width - resolution) // 2,
            height=self.explication_riviere.content_height * 1.3,
            border_color=[0, 0, 0],
            border=5,
        )

        self.explication_border.anchor_x = self.explication_border.width // 2
        self.explication_border.anchor_y = self.explication_border.height // 2

        self.label_paramètres = pyglet.text.Label(
            f"Paramètres actuels :\n\nresolution : {resolution_map}\ntaille de la grille : {grid_size}\nnombre d'octaves : {nb_octaves}\npersistance : {persistence}",
            x=self.width // 2,
            y=self.height // 2,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=1000,
            align="center",
            font_size=20,
        )

        self.label_button_generation = pyglet.text.Label(
            "GÉNÉRER LA CARTE",
            x=self.width // 2,
            y=(self.height // 2 - self.label_paramètres.content_height // 2) // 2,
            anchor_x="center",
            anchor_y="center",
            align="center",
            weight="ultrabold",
            font_size=25,
        )

        self.label_loading = pyglet.text.Label(
            "LOADING...",
            x=self.width // 2,
            y=self.height // 4,
            anchor_x="center",
            anchor_y="center",
            align="center",
            weight="ultrabold",
            font_size=25,
        )

        self.loading = False

        img = Image.open("out/carte_modified.png")
        img = img.resize((resolution, resolution), Image.NEAREST)
        img.save("out/carte_modified.png")

        self.map_sprite = pyglet.sprite.Sprite(
            pyglet.image.load("out/carte_modified.png"),
            x=(self.width // 2) - resolution // 2,
            y=(self.height // 2) - resolution // 2,
        )

        # self.map_sprite.scale_x = 1000 / self.map_sprite.image.width
        # self.map_sprite.scale_y = 1000 / self.map_sprite.image.height

        self.button_riviere = pyglet.sprite.Sprite(
            img=self.icone_riviere,
            x=(resolution + (self.width // 2 - resolution // 2) + self.width // 50),
            y=resolution,
        )
        # self.button_riviere.image.anchor_x = self.icone_riviere.width // 2
        # self.button_riviere.image.anchor_y = self.icone_riviere.height // 2

        self.button_river_is_pressed = False
        # self.label_riviere = pyglet.text.Label(
        #     "Rivières",
        #     x=(9 * (resolution // 10) + (self.width // 2 - resolution // 2)),
        #     y=resolution,
        #     anchor_x="center",
        #     anchor_y="center",
        # )

        # self.background_riviere = pyglet.shapes.BorderedRectangle(
        #     x=self.label_riviere.x - self.label_riviere.content_width // 2 - 10,
        #     y=self.label_riviere.y - self.label_riviere.content_height // 2 - 5,
        #     width=self.label_riviere.content_width + 20,
        #     height=self.label_riviere.content_height + 10,
        #     color=[146, 146, 146],
        #     border_color=[0, 0, 0],
        # )

        self.button_terraforming = pyglet.sprite.Sprite(
            pyglet.image.load("icone_terraforming.png"),
            x=(resolution + (self.width // 2 - resolution // 2) + self.width // 50),
            y=self.button_riviere.y - 3 * self.button_riviere.height // 2,
        )

        self.button_terraforming_is_pressed = False

        # self.button_border = pyglet.shapes.BorderedRectangle(
        #     x=(resolution + (self.width // 2 - resolution // 2) + self.width // 50),
        #     y=self.button_riviere.y - (self.button_riviere.y - self.button_terraforming.y) // 2,
        #     width=1.5 * self.button_riviere.width,
        #     height=(self.button_riviere.y - self.button_terraforming.y) + self.button_riviere.height + self.button_terraforming.height,
        #     border_color=[0, 0, 0],
        #     border=5,
        # )

        # self.button_border.anchor_x = self.button_border.width // 2
        # self.button_border.anchor_y = self.button_border.height // 2

        x_center = self.button_riviere.x + self.button_riviere.width // 2
        y_center = (self.button_riviere.y + self.button_terraforming.y) // 2

        self.button_border = pyglet.shapes.BorderedRectangle(
            x=x_center,
            y=y_center + self.button_terraforming.height // 2,
            width=1.25 * self.button_riviere.width,
            height=(self.button_riviere.y - self.button_terraforming.y)
            + 1.5 * self.button_riviere.height,
            border_color=[0, 0, 0],
            border=5,
        )
        self.button_border.anchor_x = self.button_border.width // 2
        self.button_border.anchor_y = self.button_border.height // 2

        # self.label_terraforming = pyglet.text.Label(
        #     "Terraforming",
        #     x=(9 * (resolution // 10) + (self.width // 2 - resolution // 2)),
        #     y=9 * (resolution // 10),
        #     anchor_x="center",
        #     anchor_y="center",
        # )

        self.terraforming_radius = 30

        self.cercle = pyglet.shapes.Circle(
            x=self.width // 2,
            y=self.height // 2,
            radius=0.8 * self.terraforming_radius,
            color=(255, 0, 0),
        )
        self.cercle.opacity = 128
        self.cercle_visible = False

        self.bruit_array = np.zeros((resolution, resolution))

        # self.image_gris = Image.open("out/image_gradient.png")
        # self.bruit_array = np.array(self.image_gris).astype(np.float32)
        # self.bruit_array /= 255.0

        self.liste_rivieres = []
        self.coordonnees_source_rivieres = []

        self.zoom = 1.0

        pyglet.clock.schedule_interval(self.update, 0.1)

    def on_draw(self):
        self.clear()
        if self.fenetre == 1:
            self.label_paramètres.draw()
            if not self.loading:
                self.label_button_generation.draw()
            if self.loading:
                self.label_loading.draw()
        elif self.fenetre == 2:
            self.explication_border.draw()
            self.button_border.draw()
            self.map_sprite.draw()
            self.button_riviere.draw()
            # self.background_riviere.draw()
            # self.label_riviere.draw()
            self.button_terraforming.draw()
            # self.label_terraforming.draw()
            if self.button_terraforming_is_pressed:
                self.cercle.draw()
                self.explication_terraforming.draw()
            if self.loading:
                self.label_loading.draw()
            if self.button_river_is_pressed:
                self.explication_riviere.draw()
            if (
                not self.button_river_is_pressed
                and not self.button_terraforming_is_pressed
            ):
                self.explication_base.draw()

    def update(self, dt):
        # self.map_sprite = pyglet.sprite.Sprite(
        #     pyglet.image.load("out/carte_modified.png"),
        #     x=(self.width // 2) - resolution // 2,
        #     y=(self.height // 2) - resolution // 2,
        # )
        # self.map_sprite.image = pyglet.image.load("out/carte_modified.png")
        self.map_sprite.draw()
        self.cercle.radius = 0.8 * self.terraforming_radius
        if self.fenetre == 1:
            self.label_button_generation.draw()
        if self.loading:
            self.label_loading.draw()

    # def update(self, dt):
    #     img = pyglet.image.load("out/carte_modified.png")
    #     self.map_sprite.image = img

    def generer_carte(self, dt):
        matrice_bruit_perlin()

        with open("image_niveau_gris.py") as f:
            exec(f.read())

        self.coefficient = image_gradient()

        image_gris = Image.open("out/image_gradient.png")
        self.bruit_array = np.array(image_gris).astype(np.float32)
        self.bruit_array /= 255.0

        couleurs(self.bruit_array, self.liste_rivieres, self.coefficient)

        img = Image.open("out/carte_modified.png")
        img = img.resize((resolution, resolution), Image.NEAREST)
        img.save("out/carte_modified.png")

        self.map_sprite.image = pyglet.image.load("out/carte_modified.png")

        self.fenetre = 2
        pyglet.gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        self.loading = False

    def ajouter_riviere(self, dt):
        if not riviere_infiltration:
            self.liste_rivieres += add_rivers(x_image, y_image, self.bruit_array, self.coefficient)

            self.coordonnees_source_rivieres.append((x_image, y_image))

            couleurs(self.bruit_array, self.liste_rivieres, self.coefficient)
        else:
            self.liste_rivieres += add_rivers_infiltration(
                x_image, y_image, self.bruit_array
            )

            self.coordonnees_source_rivieres.append((x_image, y_image))

            couleurs(self.bruit_array, self.liste_rivieres, self.coefficient)

        img = Image.open("out/carte_modified.png")
        img = img.resize((resolution, resolution), Image.NEAREST)
        img.save("out/carte_modified.png")

        self.map_sprite.image = pyglet.image.load("out/carte_modified.png")
        self.loading = False

    def ajouter_terraforming(self, button):
        if button == 1:
            terraforming(
                x_image,
                y_image,
                int(self.terraforming_radius * (resolution_map / resolution)),
                -0.2,
                self.bruit_array,
            )
        elif button == 4:
            terraforming(
                x_image,
                y_image,
                int(self.terraforming_radius * (resolution_map / resolution)),
                0.2,
                self.bruit_array,
            )
        elif button == 2:
            terraforming(
                x_image,
                y_image,
                int(self.terraforming_radius * (resolution_map / resolution)),
                0.05,
                self.bruit_array,
                plane=True,
            )

        self.liste_rivieres = []
        for case in self.coordonnees_source_rivieres:
            self.liste_rivieres += add_rivers(case[0], case[1], self.bruit_array, self.coefficient)

        couleurs(self.bruit_array, self.liste_rivieres, self.coefficient)

        img = Image.open("out/carte_modified.png")
        img = img.resize((resolution, resolution), Image.NEAREST)
        img.save("out/carte_modified.png")

        self.map_sprite.image = pyglet.image.load("out/carte_modified.png")
        self.loading = False

    def on_mouse_press(self, x, y, button, modifiers):
        print(button)
        if self.fenetre == 1:
            if (
                abs(self.label_button_generation.x - x)
                <= self.label_button_generation.content_width / 2
            ) and (
                abs(self.label_button_generation.y - y)
                <= self.label_button_generation.content_height / 2
            ):
                self.loading = True
                self.dispatch_event("on_draw")
                print("loading...")
                pyglet.clock.schedule_once(self.generer_carte, 0.1)

                # for i in range(1000):
                #     pyglet.clock.tick()

                # matrice_bruit_perlin()

                # with open("image_niveau_gris.py") as f:
                #     exec(f.read())

                # image_gradient()

                # image_gris = Image.open("out/image_gradient.png")
                # self.bruit_array = np.array(image_gris).astype(np.float32)
                # self.bruit_array /= 255.0

                # couleurs(self.bruit_array, self.liste_rivieres)

                # self.fenetre = 2
                # pyglet.gl.glClearColor(1.0, 1.0, 1.0, 1.0)

        elif self.fenetre == 2:
            self.label_loading.color = [0, 0, 0]
            # print(x, y)
            global x_image
            global y_image
            x_image = int(
                (x - (self.width // 2 - resolution // 2)) * resolution_map / resolution
            )
            y_image = resolution_map - int(
                (y - (self.height // 2 - resolution // 2)) * resolution_map / resolution
            )
            print(x_image, y_image)
            if (0 <= x - self.button_riviere.x <= self.button_riviere.width) and (
                0 <= y - self.button_riviere.y <= self.button_riviere.height
            ):
                self.button_terraforming.image = self.icone_terraforming
                self.button_terraforming_is_pressed = False

                if self.button_river_is_pressed is not True:
                    self.button_riviere.image = self.icone_riviere_clique
                    self.button_river_is_pressed = True
                else:
                    self.button_riviere.image = self.icone_riviere
                    self.button_river_is_pressed = False

            elif (
                0 <= x - self.button_terraforming.x <= self.button_terraforming.width
            ) and (
                0 <= y - self.button_terraforming.y <= self.button_terraforming.height
            ):
                self.button_riviere.image = self.icone_riviere
                self.button_river_is_pressed = False

                if self.button_terraforming_is_pressed is not True:
                    self.button_terraforming.image = self.icone_terrfaforming_clique
                    self.button_terraforming_is_pressed = True
                else:
                    self.button_terraforming.image = self.icone_terraforming
                    self.button_terraforming_is_pressed = False

            elif self.button_river_is_pressed is True:
                self.loading = True

                pyglet.clock.schedule_once(self.ajouter_riviere, 0.1)

                # image_gris = Image.open("out/image_gradient.png")

                # bruit_array = np.array(image_gris).astype(np.float32)

                # bruit_array = bruit_array / 255.0

                # if not riviere_infiltration:
                #     self.liste_rivieres += add_rivers(
                #         x_image, y_image, self.bruit_array
                #     )

                #     self.coordonnees_source_rivieres.append((x_image, y_image))

                #     couleurs(self.bruit_array, self.liste_rivieres)
                # else:
                #     self.liste_rivieres += add_rivers_infiltration(
                #         x_image, y_image, self.bruit_array
                #     )

                #     self.coordonnees_source_rivieres.append((x_image, y_image))

                #     couleurs(self.bruit_array, self.liste_rivieres)
                # self.loading = False

            elif self.button_terraforming_is_pressed is True:
                self.loading = True

                pyglet.clock.schedule_once(
                    lambda dt: self.ajouter_terraforming(button), 0.1
                )

                # print("start")
                # image_gris = Image.open("out/image_gradient.png")

                # bruit_array = np.array(image_gris).astype(np.float32)

                # bruit_array /= 255
                # if button == 1:
                #     terraforming(
                #         x_image,
                #         y_image,
                #         self.terraforming_radius,
                #         -0.2,
                #         self.bruit_array,
                #     )
                # elif button == 4:
                #     terraforming(
                #         x_image,
                #         y_image,
                #         self.terraforming_radius,
                #         0.2,
                #         self.bruit_array,
                #     )
                # elif button == 2:
                #     terraforming(
                #         x_image,
                #         y_image,
                #         self.terraforming_radius,
                #         0.2,
                #         self.bruit_array,
                #         plane=True,
                #     )

                # self.liste_rivieres = []
                # for case in self.coordonnees_source_rivieres:
                #     self.liste_rivieres += add_rivers(
                #         case[0], case[1], self.bruit_array
                #     )

                # couleurs(self.bruit_array, self.liste_rivieres)
                # self.loading = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.cercle.x = x
        self.cercle.y = y
        if self.button_terraforming_is_pressed is True:
            self.cercle.visible = True
        else:
            self.cercle.visible = False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.button_terraforming_is_pressed is True:
            self.terraforming_radius += 5 * scroll_y
            self.terraforming_radius = max(5, self.terraforming_radius)
            self.terraforming_radius = min(resolution // 2, self.terraforming_radius)
        # else:
        #     zoom_step = 0.1
        #     self.zoom += scroll_y * zoom_step
        #     self.map_sprite.scale = self.zoom
        #     # self.map_sprite.x = (self.width // 2) - (self.map_sprite.width // 2)
        #     # self.map_sprite.y = (self.height // 2) - (self.map_sprite.height // 2)
        #     self.map_sprite.x = x
        #     self.map_sprite.y = y


window = MapGenerator()
# print(window.get_size())

pyglet.app.run()
print("c'est fini !")
