import math
from abc import ABC, abstractmethod
from typing import Optional
from utils.boundingbox import BoundingBox
from vectormath import Vector3
from utils.intersection import Intersection
from utils.interval import Interval
from utils.ray import Ray


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
    def intersect(self, ray, ray_dist_interval):
        pass


class Sphere(Primitive):

    def __init__(self, origin, radius, material) -> None:
        super().__init__("sphere")
        self.origin = origin
        self.radius = radius
        self.material = material
        vec = Vector3(radius, radius, radius)
        bbox = BoundingBox()
        bbox.from_vectors(origin - vec, origin + vec)
        self.boundingbox = bbox

    def __str__(self):
        return "{}: origin:{}, radius: {}, material: {}".format(self.name, self.origin, self.radius, self.material)

    def intersect(self, ray, ray_dist_interval):

        oc = ray.origin - self.origin
        a = ray.direction.length ** 2
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
        u = phi / (2 * math.pi)
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
        a = ray.direction.length ** 2
        half_b = oc.dot(ray.direction)
        c = oc.length ** 2 - self.radius ** 2
        disc = half_b * half_b - a * c
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
        isect.set_face_normal(ray, outward_normal)
        isect.material = self.material
        isect.object = self
        return isect

    def center(self, time):
        return self.center_start + time * self.center_end


class Rectangle(Primitive):
    def __init__(self, min_point, max_point, k, material, axis='xy'):
        super().__init__("rectangle_primitive")
        self.min_point = min_point
        self.max_point = max_point
        self.k = k
        self.material = material
        self.axis = axis
        self._build_boundingbox()

    def intersect(self, ray, ray_dist_interval):
        if self.axis == 'xy':
            t = (self.k - ray.origin.z) / ray.direction.z
            if t < ray_dist_interval.min_dist or t > ray_dist_interval.max_dist:
                return None
            x = ray.origin.x + t * ray.direction.x
            y = ray.origin.y + t * ray.direction.y
            if x < self.min_point[0] or x > self.min_point[1] or y < self.max_point[0] or y > self.max_point[1]:
                return None
            isect = Intersection()
            isect.distance = t
            u = (x - self.min_point[0])/(self.min_point[1]-self.min_point[0])
            v = (y - self.max_point[0])/(self.max_point[1] - self.max_point[0])
            isect.uv_coordinates = (u,v)
            out_normal = Vector3(0,0,1)
            isect.set_face_normal(ray, out_normal)
            isect.material = self.material
            isect.primitive = self
            isect.point = ray.evaluate(t)
            return isect
        elif self.axis == 'yz':
            t = (self.k - ray.origin.x) / ray.direction.x
            if t < ray_dist_interval.min_dist or t > ray_dist_interval.max_dist:
                return None
            y = ray.origin.y + t * ray.direction.y
            z = ray.origin.z + t * ray.direction.z
            if y < self.min_point[0] or y > self.min_point[1] or z < self.max_point[0] or z > self.max_point[1]:
                return None
            isect = Intersection()
            isect.distance = t
            u = (y - self.min_point[0]) / (self.min_point[1] - self.min_point[0])
            v = (z - self.max_point[0]) / (self.max_point[1] - self.max_point[0])
            isect.uv_coordinates = (u, v)
            out_normal = Vector3(1, 0, 0)
            isect.set_face_normal(ray, out_normal)
            isect.material = self.material
            isect.primitive = self
            isect.point = ray.evaluate(t)
            return isect
        elif self.axis == 'xz':
            t = (self.k - ray.origin.y) / ray.direction.y
            if t < ray_dist_interval.min_dist or t > ray_dist_interval.max_dist:
                return None
            x = ray.origin.x + t * ray.direction.x
            z = ray.origin.z + t * ray.direction.z
            if x < self.min_point[0] or x > self.min_point[1] or z < self.max_point[0] or z > self.max_point[1]:
                return None
            isect = Intersection()
            isect.distance = t
            u = (x - self.min_point[0]) / (self.min_point[1] - self.min_point[0])
            v = (z - self.max_point[0]) / (self.max_point[1] - self.max_point[0])
            isect.uv_coordinates = (u, v)
            out_normal = Vector3(0, 1, 0)
            isect.set_face_normal(ray, out_normal)
            isect.material = self.material
            isect.primitive = self
            isect.point = ray.evaluate(t)
            return isect
        return None

    def _build_boundingbox(self):
        if self.axis == 'xy':
            self.boundingbox = BoundingBox()
            self.boundingbox.from_vectors(Vector3(self.min_point[0], self.max_point[0], self.k + 0.0001),
                                          Vector3(self.min_point[1], self.max_point[1], self.k + 0.0001))
        elif self.axis == 'yz':
            self.boundingbox = BoundingBox()
            self.boundingbox.from_vectors(Vector3(self.k + 0.0001, self.min_point[0], self.max_point[0]),
                                          Vector3(self.k + 0.0001, self.min_point[1], self.max_point[1]))

        elif self.axis == 'xz':
            self.boundingbox = BoundingBox()
            self.boundingbox.from_vectors(Vector3(self.min_point[0], self.k + 0.0001, self.max_point[0]),
                                          Vector3(self.min_point[1], self.k + 0.0001, self.max_point[1]))


class Box(Primitive):
    def __init__(self, box_min, box_max, material,offset=Vector3(0,0,0)):
        super().__init__("box")
        self.boundingbox = BoundingBox()
        self.boundingbox.from_vectors(box_min + offset, box_max + offset)

        self.box_min = box_min + offset
        self.box_max = box_max + offset

        self.sides = PrimitiveList()
        self.sides.add(Rectangle((box_min.x,box_max.x),(box_min.y, box_max.y),box_max.z,material,'xy'))
        self.sides.add(Rectangle((box_min.x,box_max.x),(box_min.y, box_max.y),box_min.z,material,'xy'))

        self.sides.add(Rectangle((box_min.x,box_max.x),(box_min.z,box_max.z),box_max.y,material,'xz'))
        self.sides.add(Rectangle((box_min.x,box_max.x),(box_min.z,box_max.z),box_min.y,material,'xz'))

        self.sides.add(Rectangle((box_min.y,box_max.y),(box_min.z,box_max.z),box_max.x,material,'yz'))
        self.sides.add(Rectangle((box_min.y,box_max.y),(box_min.z,box_max.z),box_min.x,material,'yz'))

        self.translate_offset = offset

    def intersect(self, ray, ray_dist_interval):
        # this includes translate algorithm

        moved_ray = Ray(ray.origin - self.translate_offset, ray.direction, ray.time)
        isect = self.sides.intersect(moved_ray, ray_dist_interval)
        if isect is not None:
            isect.point = isect.point + self.translate_offset
            isect.set_face_normal(moved_ray, isect.normal)
        return isect


class PrimitiveList(Primitive):

    def __init__(self, obj=None):
        super().__init__('primitive_list')
        if obj is None:
            self.objects = []
            self.boundingbox = BoundingBox()
        else:
            self.objects = []
            self.boundingbox = BoundingBox()
            self.add(obj)

    def __str__(self):
        return "PrimitiveList items count: %s" % len(self.objects)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, idx):
        return self.objects[idx]

    def clear(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        bbox = BoundingBox()
        bbox.from_boundingbox(self.boundingbox, obj.boundingbox)
        self.boundingbox = bbox

    def intersect(self, ray, ray_dist_interval):
        isect = None
        # found = False
        closest = ray_dist_interval.max_dist
        for obj in self.objects:
            o = obj.intersect(ray, Interval(ray_dist_interval.min_dist, closest))
            if o is not None:
                # found = True
                closest = o.distance
                isect = o

        return isect
