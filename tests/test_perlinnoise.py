import unittest
from utils.perlin import PerlinNoise
from vectormath import Vector3


class TestPerlinNoiseTestCase(unittest.TestCase):

    def setUp(self):
        self.pn = PerlinNoise()

    def test_perlinnoise_noise(self):
        val = self.pn.noise(Vector3(0, 0, 0))

        print(val)
        self.assertTrue(0. < val < 1., "does not fall within range [0..1]")

    def test_perlinnoise_vnoise(self):
            val = self.pn.vector_noise(Vector3(0, 0.98188283884, 0))

            print(val)
            self.assertTrue(-1. < val < 1., "does not fall within range [0..1]")

