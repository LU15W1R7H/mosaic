import os
from PIL import Image

res_path = os.getcwd() + "/res"
mosaic_size = 200
big_size = 100

# load big
big = Image.open(res_path + "/big.png")
big = big.resize((big_size, big_size), Image.ANTIALIAS)

# load palette
palette = []
palette_path = res_path + "/palette"
for file in os.listdir(palette_path):
    im = Image.open(palette_path + "/" + file)
    print("opened " + file)
    im = im.resize((mosaic_size, mosaic_size), Image.ANTIALIAS)
    palette.append(im)
print("loaded " + str(len(palette)) + " images")

# compute average of pallete images
palette_color = []
for mosaic in palette:
    average = mosaic.resize((1, 1), Image.ANTIALIAS)
    average = average.getpixel((0, 0))
    palette_color.append(average)

# final image
final_image = Image.new(
    'RGB', (big_size * mosaic_size, big_size * mosaic_size))

for y in range(0, big.height):
    print("Progress: " + str(y / big.height))
    for x in range(0, big.width):
        big_color = big.getpixel((x, y))

        min_diff = float('inf')
        best_index = -1
        for imosaic, mosaic_color in enumerate(palette_color):
            diff = 0.0
            for icomp in range(0, 3):
                diff += (big_color[icomp] - mosaic_color[icomp])**2
            if (diff < min_diff):
                min_diff = diff
                best_index = imosaic

        final_image.paste(palette[best_index],
                          (mosaic_size * x, mosaic_size * y))

final_image.save(res_path + "/mosaic.png")
