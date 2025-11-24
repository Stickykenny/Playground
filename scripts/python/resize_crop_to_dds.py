"""
This script resize and crop image into a target width and height.
It then converts it into a .dds file

No current library support this specific compression format so I'm using a external tool
Alternative already exists but it requires an NVIDIA tool that I don't have access to
"""

from wand.image import Image
import subprocess
import os
# https://docs.wand-py.org/en/0.6.12/guide/resizecrop.html#crop-images

target_folder = "fg"

wanted_width = 1024
wanted_height = 1412

for root, dirs, files in os.walk(target_folder):
    for file in files:
        print(os.path.join(root, file))
        filepath = os.path.join(root, file)

        if file.endswith('.png') or file.endswith('.jpg'):
            with Image(filename=filepath) as img:

                print(img.compression)
                original_dim = img.size
                print(original_dim)
                origin_width, origin_height = original_dim
                ratio = origin_width / origin_height

                wanted_ratio = wanted_width / wanted_height
                print(wanted_ratio)
                print(ratio)

                if (wanted_height / origin_height) > (wanted_width / origin_width):
                    mult = wanted_height / origin_height
                    img.resize(int(origin_width * mult), int(origin_height * mult))
                else:
                    mult = wanted_width / origin_width
                    img.resize(int(origin_width * mult), int(origin_height * mult))

                print(img.size)

                new_width, new_height = img.size

                if (new_width > wanted_width):
                    diff = new_width - wanted_width
                    left = 0 + diff // 2
                    right = new_width - (diff + 1) // 2
                    img.crop(left, 0, right, new_height)

                if (new_height > wanted_height):
                    diff = new_height - wanted_height
                    top = 0 + diff // 2
                    bottom = new_height - (diff + 1) // 2
                    img.crop(0, top, new_width, bottom)

                print(img.size)

                filepath = filepath.replace(".", "") + "_cleaned"
                img.save(filename=filepath)
                cmd = [
                    "texconv",
                    "-f", "BC7_UNORM_SRGB", "-y", "-srgb",
                    "-o", target_folder,
                    filepath
                ]
                print(cmd)
                subprocess.run(cmd, check=True)
                os.remove(filepath)

        print("----------")


"""
texconv -f BC7_UNORM_SRGB -o output_folder input.png
"""
