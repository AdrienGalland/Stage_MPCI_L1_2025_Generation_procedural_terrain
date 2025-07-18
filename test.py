import pyglet
from pyglet.gl import GL_NEAREST

from PIL import Image

img = Image.open("out/carte_modified.png")
img = img.resize((1000, 1000), Image.NEAREST)
img.save("out/carte_modified.png")

window = pyglet.window.Window(width=1200, height=1000)

img_data = pyglet.image.load("out/carte_modified.png")
texture = img_data.get_texture()

sprite = pyglet.sprite.Sprite(
    texture,
    x=(window.width // 2) - 500,
    y=(window.height // 2) - 500
)
sprite.scale_x = 1000 / texture.width
sprite.scale_y = 1000 / texture.height

@window.event
def on_draw():
    window.clear()
    sprite.draw()

print(texture.width, texture.height)

pyglet.app.run()
