from typing import Optional
from utils.boundingbox import BoundingBox

from utils.intersection import Intersection
from utils.interval import Interval
from utils.shapes import Primitive

#
# class PrimitiveList(Primitive):
#
#     def __init__(self, obj=None):
#         super().__init__('primitive_list')
#         if obj is None:
#             self.objects = []
#             self.boundingbox = BoundingBox()
#         else:
#             self.objects = []
#             self.boundingbox= BoundingBox()
#             self.add(obj)
#
#
#     def __str__(self):
#         return "PrimitiveList items count: %s" % len(self.objects)
#     def __len__(self):
#         return len(self.objects)
#
#     def __getitem__(self, idx):
#         return self.objects[idx]
#
#     def clear(self):
#         self.objects = []
#
#     def add(self, obj):
#         self.objects.append(obj)
#         bbox = BoundingBox()
#         bbox.from_boundingbox(self.boundingbox, obj.boundingbox)
#         self.boundingbox = bbox
#
#     def intersect(self, ray, ray_dist_interval) -> Optional[Intersection]:
#         isect = None
#         # found = False
#         closest = ray_dist_interval.max_dist
#         for obj in self.objects:
#             o = obj.intersect(ray, Interval(ray_dist_interval.min_dist, closest))
#             if o is not None:
#                 # found = True
#                 closest = o.distance
#                 isect = o
#
#         return isect
