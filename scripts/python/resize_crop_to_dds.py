
from wand.image import Image
from wand.display import display
import os
# traverse whole directory
for root, dirs, files in os.walk("fold"):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.png') or file.endswith('.jpg'):
            # print whole path of files
            print(os.path.join(root, file))
            filepath = os.path.join(root, file)
            with Image(filename=filepath) as img:
                print(filepath)
                img.compression = 'dxt5'
                img.save(filename='your.dds')

                original_dim = img.size
                print(original_dim)
                origin_width, origin_height = original_dim
                ratio = origin_width / origin_height

                wanted_width = 1024
                wanted_height = 1412
                wanted_ratio = wanted_width / wanted_height
                print(wanted_ratio)
                print(ratio)

                if (wanted_height / origin_height) > (wanted_width / origin_width):
                    mult = wanted_height / origin_height
                    img.resize(int(origin_width * mult), int(origin_height * mult))
                else:
                    mult = wanted_width / origin_width
                    img.resize(int(origin_width * mult), int(origin_height * mult))

                """if wanted_ratio < ratio:
                    img.resize(int(wanted_height * ratio), wanted_height)
                else:
                    img.resize(int(origin_width), int(wanted_width * ratio))"""

                print(img.size)

                new_width, new_height = img.size
                left = max(0, (new_width - wanted_width) // 2)
                top = max(0, (new_height - wanted_height) // 2)
                right = min(origin_width, (left + wanted_width))
                bottom = min(origin_height, (top + wanted_height))
                print([top, left, right, bottom])
                img.crop(left, top, right, bottom)
                print(img.size)

                img.compression = 'dxt5'
                filepath = filepath.replace(".png", ".dds")
                filepath = filepath.replace(".jpg", ".dds")

                img.save(filename=filepath)
                # https://docs.wand-py.org/en/0.6.12/guide/resizecrop.html#crop-images

    """for r in 1, 2, 3:
        with img.clone() as i:
            i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
            i.rotate(90 * r)
            i.save(filename='mona-lisa-{0}.png'.format(r))
            display(i)"""
