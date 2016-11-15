from unittest import TestCase
from io import BytesIO
from base64 import b16decode


from visual_cryptography.visual_cryptography import ImageLayer, produce_image_layer_from_real_image



class TestImageLayer(TestCase):
    test_data = b'000001000100101010000100040028010000160000002800000010000000200000000100040000000000800000000000000000000000100000000000000000000000FF84000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111100000010000000010000001000000001000000000000000000000000000000000000000000000000000000000000000000000011100001110000001110000111000000111000011100000000000000000000000000000000000FFFF0000FFFF0000FFFF0000FFFF0000E0070000EFF70000EFF70000FFFF0000FFFF0000FFFF0000FFFF0000E3C70000E3C70000E3C70000FFFF0000FFFF0000'

    def get_test_image(self):
        return BytesIO(b16decode(self.test_data))


    def test_produce_image_layer_from_real_image(self):
        img = produce_image_layer_from_real_image(self.get_test_image())
        self.assertEqual(img.data[2][3], 0)
        self.assertEqual(img.data[0][0], 0)


    def test_get_empty_data(self):
        img = ImageLayer(0, 0)
        m = img.get_empty_data(2, 3)
        self.assertEqual(len(m), 2)
        self.assertEqual(len(m[0]), 3)

    def test_produce_empty_shares(self):
        img = ImageLayer(5, 6)
        ret = img.produce_empty_shares()

        two_shares = 2
        self.assertEqual(len(ret), two_shares)

        ten_pixels_width = 10
        self.assertEqual(len(ret[0]), ten_pixels_width)

        twelve_pixels_height = 12
        self.assertEqual(len(ret[0][0]), twelve_pixels_height)


    def test_place_sub_pixels_in_shares_position(self):
        img = ImageLayer(2, 3)
        shares = img.produce_empty_shares()

        c = [[1, 1, 1, 1],[1, 1, 1, 1]]
        img.place_sub_pixels_in_shares(1,1, shares, c)

        self.assertListEqual(shares[0][0].tolist(), [0,0,0,0,0,0])
        self.assertListEqual(shares[0][1].tolist(), [0,0,0,0,0,0])
        self.assertListEqual(shares[0][2].tolist(), [0,0,1,1,0,0])
        self.assertListEqual(shares[0][3].tolist(), [0,0,1,1,0,0])

    def test_place_sub_pixels_in_shares(self):
        img = ImageLayer(2, 3)
        shares = img.produce_empty_shares()

        c = [[1, 0, 0, 1],[0, 1, 0, 1]]
        img.place_sub_pixels_in_shares(1,1, shares, c)
        self.assertListEqual(shares[0][0].tolist(), [0,0,0,0,0,0])
        self.assertListEqual(shares[0][1].tolist(), [0,0,0,0,0,0])
        self.assertListEqual(shares[0][2].tolist(), [0,0,1,0,0,0])
        self.assertListEqual(shares[0][3].tolist(), [0,0,0,1,0,0])

    def test_get_pixel_value_in_share(self):
        img = ImageLayer(10, 10)
        share = img.produce_empty_shares()[0]

        pixel = [1, 2, 3, 4]
        img.place_sub_pixels_in_shares(3,1, [share], [pixel])
        self.assertEqual(pixel, img.get_pixel_value_in_share(3,1, share))

    def test_inverse_pixel(self):
        img = ImageLayer(2, 3)
        inv = img.inverse_pixel([0, 1])
        expt = [1, 0]
        self.assertEqual(expt, inv)

    def test_produce_cheated_image_from_other_share(self):
        img = produce_image_layer_from_real_image(self.get_test_image())
        share = img.produce_two_shares_from_image()[0]

        cheated_share = img.produce_cheated_image_from_other_share(share)
        self.assertEqual(len(cheated_share), 32)
        self.assertEqual(len(cheated_share[0]), 32)

    def test_produce_two_shares_from_image(self):
        img = produce_image_layer_from_real_image(self.get_test_image())
        shares = img.produce_two_shares_from_image()
        self.assertEquals(len(shares), 2)
