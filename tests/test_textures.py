import unittest

from vectormath import Vector3

from utils.colors import RGBColor
from utils.perlin import PerlinNoise
from utils.textures import Perlin


class TestTexturesTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.txt = Perlin(1.0, PerlinNoise())

    def test_PerlinTexture(self):
        val = self.txt.value(None, Vector3(0, 0, 0))
        print(val)
        self.assertIsInstance(val, RGBColor)


if __name__ == '__main__':
    unittest.main()
