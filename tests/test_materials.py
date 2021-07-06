import unittest

from utils.intersection import Intersection
from utils.materials import Diffuse
from utils.textures import Perlin
from vectormath import Vector3


class MaterialsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.matperlin = Diffuse(Perlin(4))
        self.isect = Intersection()

    def test_perlinmaterial(self):
        val = self.matperlin.scatter(Vector3(0.98, 0, 0.78), )
        print(val)
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
