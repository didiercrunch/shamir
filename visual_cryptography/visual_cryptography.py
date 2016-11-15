from PIL import Image
import numpy as np
from json import dumps
from random import choice


class ImageLayer(object):
    c_0 = (
        [[0,0,1,1], [0,0,1,1]],
        [[1,1,0,0], [1,1,0,0]],
        [[1,0,1,0], [1,0,1,0]],
        [[0,1,0,1], [0,1,0,1]],
        [[0,1,1,0], [0,1,1,0]],
        [[1,0,0,1], [1,0,0,1]],
    )

    c_1 = (
        [[0,0,1,1], [1,1,0,0]],
        [[1,1,0,0], [0,0,1,1]],
        [[1,0,1,0], [0,1,0,1]],
        [[0,1,0,1], [1,0,1,0]],
        [[0,1,1,0], [1,0,0,1]],
        [[1,0,0,1], [0,1,1,0]],
    )

    pixel_width = 2

    def __init__(self, height, width):
        self.data = self.get_empty_data(height, width)

    def get_json_string(self):
        return dumps(self.data)

    def get_empty_data(self, number_of_lines, number_of_columns):
        data = []
        for i in range(number_of_lines):
            data.append(np.array([0]*number_of_columns))
        return np.array(data)

    def produce_empty_shares(self):
        sub_pixel_matrix = self.c_0[0]
        number_of_share_to_produce = len(sub_pixel_matrix)
        number_of_sub_pixels = len(sub_pixel_matrix[0])

        current_width = len(self.data[0])
        current_height = len(self.data)

        ret = [self.get_empty_data(current_height * self.pixel_width, current_width * self.pixel_width) for i in range(len(sub_pixel_matrix))]
        return ret

    def get_single_empty_share(self):
        return self.produce_empty_shares()[0]

    def place_sub_pixels_in_shares(self, line, col, shares, sub_pixel_matrix):
        number_of_sub_pixels = len(sub_pixel_matrix[0])
        for i, share in enumerate(shares):
            for l in range(line * self.pixel_width, (line + 1) * self.pixel_width ):
                for c in range(col * self.pixel_width, (col + 1) * self.pixel_width):
                    share[l][c] = sub_pixel_matrix[i][(l % self.pixel_width) * self.pixel_width + (c % self.pixel_width)]

    def get_pixel_value_in_share(self, x, y, share):
        pixel = [0, 0, 0, 0]
        pixel[0] = share[2 * x][2 * y]
        pixel[1] = share[2 * x][2 * y + 1]
        pixel[2] = share[2 * x + 1][2 * y]
        pixel[3] = share[2 * x + 1][2 * y + 1]
        return pixel

    def produce_shares_from_image(self):
        shares = self.produce_empty_shares()
        for (x,y), color in np.ndenumerate(self.data):
            c = self.c_0 if color == 0 else self.c_1
            self.place_sub_pixels_in_shares(x, y, shares, choice(c))
        return shares

    def produce_two_shares_from_image(self):
        return self.produce_shares_from_image()

    def inverse_pixel(self, pixel):
        return [(e + 1) % 2 for e in pixel]

    def get_cheated_pixel(self, x, y, share, color):
        pixel = self.get_pixel_value_in_share(x, y, share)
        if color == 0:
            return pixel
        return self.inverse_pixel(pixel)

    def produce_cheated_image_from_other_share(self, share):
        cheated_share = self.get_single_empty_share()
        for (x,y), color in np.ndenumerate(self.data):
            cheated_pixel = self.get_cheated_pixel(x, y, share, color)
            self.place_sub_pixels_in_shares(x, y, [cheated_share], [cheated_pixel])
        return cheated_share


def cmyk_to_luminance(r, g, b, a):
    """
    takes a RGB color and returns it grayscale value.  See
    http://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/
    for more information
    """
    if (r, g, b) == (0, 0, 0):
        return a
    return (0.299 * r + 0.587 * g + 0.114 * b) * a / 255


def cmyk_to_black_and_white(r, g, b, a):
    black_threshold = 255 / 2
    if cmyk_to_luminance(r, g, b, a) < black_threshold:
        return 0
    return 1


def produce_image_layer_from_real_image(image_path):
    im = Image.open(image_path).convert('RGBA')
    ret = ImageLayer(*im.size)
    d = {}
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r, g, b, a = im.im.getpixel((i,j))
            d[(r, g, b, a)] = cmyk_to_black_and_white(r, g, b, a)
            ret.data[j][i] = cmyk_to_black_and_white(r, g, b, a)
    return ret


if __name__ == '__main__':
    print(produce_image_layer_from_real_image('dog-512.png'))
