import unittest

from vectormath.vector import Vector3
from utils.shapes import Sphere
from utils.boundingvolume import BoundingVolumeNode


class TestBoundingVolumeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.sphere0 = Sphere(Vector3(0,0,-1),0.5,None)
        self.sphere1 = Sphere(Vector3(0,1,-2),0.5,None)
        self.sphere3 = Sphere(Vector3(1,2,-4),0.5, None)
        self.sphere4 = Sphere(Vector3(10,2,-5),0.5, None)
        self.list2 = [self.sphere0,self.sphere1]
        self.list3 = [self.sphere0,self.sphere1,self.sphere3]
        self.list4 = [self.sphere0,self.sphere1,self.sphere3, self.sphere4]
    
    def test_bvhcreation(self):
        bvh = BoundingVolumeNode(self.list2)
        bvh1 = BoundingVolumeNode(self.list3)
        bvh2 = BoundingVolumeNode(self.list4)

        print(bvh)