import math
from abc import ABC, abstractmethod
from typing import Optional
from utils.boundingbox import BoundingBox
from vectormath import Vector3
from utils.intersection import Intersection


class Primitive(ABC):

    def __init__(self, name='primitive') -> None:
        self.material = None
        self.boundingbox = None
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Primitive: %s" % self.name

    @abstractmethod
    def intersect(self, ray, ray_dist_interval) -> Optional[Intersection]:
        pass


class Sphere(Primitive):

    def __init__(self, origin, radius, material) -> None:
        super().__init__("sphere")
        self.origin = origin
        self.radius = radius
        self.material = material
        vec = Vector3(radius, radius,radius)
        bbox = BoundingBox()
        bbox.from_vectors(origin - vec, origin + vec)
        self.boundingbox = bbox

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
        isect.uv_coordinates = self.uv_coordinates(out_normal)

        return isect

    def uv_coordinates(self, point):
        theta = math.acos(-point.y)
        phi = math.atan2(-point.z, point.x) + math.pi
        u = phi / (2*math.pi)
        v = theta / math.pi
        return (u, v)

class MovingSphere(Primitive):

    def __init__(self, center_start, center_end, radius, material) -> None:
        super().__init__(name="moving_sphere")
        self.center_start = center_start
        self.center_end = center_end
        self.radius = radius
        self.material = material
        self.center_vector = center_end - center_start
        vec = Vector3(radius, radius, radius)
        bbox0 = BoundingBox()
        bbox0.from_vectors(self.center_start - vec, self.center_start + vec)
        bbox1 = BoundingBox()
        bbox1.from_vectors(self.center_end - vec, self.center_end + vec)
        bbox = BoundingBox()
        bbox.from_boundingbox(bbox0, bbox1)
        self.boundingbox = bbox

    def intersect(self, ray, ray_dist_interval) -> Optional[Intersection]:
        oc = ray.origin - self.center(ray.time)
        a = ray.direction.length**2
        half_b = oc.dot(ray.direction)
        c = oc.length**2 - self.radius**2
        disc = half_b*half_b  - a*c
        sqrtd = math.sqrt(disc)
        if disc < 0:
            return None
        root = (-half_b - sqrtd) / a
        if not ray_dist_interval.contains(root):
            root = (-half_b + sqrtd) / a
            if not ray_dist_interval.contains(root):
                return None
        isect = Intersection()
        isect.distance = root
        isect.point = ray.evaluate(root)
        outward_normal = (isect.point - self.center(ray.time)) / self.radius
        isect.set_face_normal(outward_normal)
        isect.material = self.material
        isect.object = self
        return isect

    def center(self, time):
        return self.center_start + time * self.center_end


class Rectangle(Primitive):
    pass

class Box(Primitive):

