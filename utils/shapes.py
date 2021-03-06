import math
from abc import ABC, abstractmethod
from typing import Optional

from utils.intersection import Intersection


class Primitive(ABC):

    def __init__(self, name='primitive') -> None:
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Primitive: %s" % self.name

    @abstractmethod
    def intersect(self, ray, ray_minmax_dist) -> Optional[Intersection]:
        pass


class Sphere(Primitive):

    def __init__(self, origin, radius, material) -> None:
        super().__init__("sphere")
        self.origin = origin
        self.radius = radius
        self.material = material

    def __str__(self):
        return "{}: origin:{}, radius: {}, material: {}".format(self.name, self.origin, self.radius, self.material)

    def intersect(self, ray, ray_dist_interval):

        oc = ray.origin - self.origin
        a = ray.direction.length**2
        half_b = ray.direction.dot(oc)  # 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius ** 2
        disc = half_b ** 2 - a * c

        if disc < 0:
            return None
        sqrtd = math.sqrt(disc)
        root = (-half_b - sqrtd) / a
        if not ray_dist_interval.contains(root):
            root = (-half_b + sqrtd) / a
            if not ray_dist_interval.contains(root):
                return None

        isect = Intersection()
        isect.distance = root
        isect.point = ray.evaluate(root)
        out_normal = (isect.point - self.origin) / self.radius
        isect.set_face_normal(ray, out_normal)
        isect.primitive = self
        isect.material = self.material

        return isect
