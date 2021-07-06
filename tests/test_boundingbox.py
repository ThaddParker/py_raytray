import unittest
from utils.boundingbox import BoundingBox
from vectormath import Vector3


class TestBoundingBoxTestCase(unittest.TestCase):

    def test_boundingboxbuild(self):
        b = BoundingBox()
        b.from_vectors(Vector3(0,0,0),Vector3(1,13,1))

        print(b)
