from PIL import Image
import numpy as np
import json

f = open("out/grayscale.json", "r")

bruit_array = np.array(json.load(f))


# bruit_array = (bruit_array - np.min(bruit_array)) / (
#     np.max(bruit_array) - np.min(bruit_array)
# )

gray_level = (bruit_array * 255).astype(np.uint8)

image = Image.fromarray(gray_level, mode='L')

image.save("out/image.png")
