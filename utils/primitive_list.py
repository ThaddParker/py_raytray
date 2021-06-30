from typing import Optional

from utils.intersection import Intersection
from utils.interval import Interval
from utils.shapes import Primitive


class PrimitiveList(Primitive):

    def __init__(self):
        super().__init__('primitive_list')
        self.objects = []

    def __str__(self):
        return "PrimitiveList items count: %s" %len(self.objects)

    def clear(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def intersect(self, ray, ray_dist_interval) -> Optional[Intersection]:
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
