from typing import Optional
import math
from utils.boundingbox import BoundingBox

from vectormath.vector import Vector3
from utils.interval import Interval
from utils.shapes import Primitive
from utils.functs import random_int


def box_compare(a: Primitive, b: Primitive, axis):
    return a.bounding_box.axis(axis).min_dist < b.bounding_box.axis(axis).min_dist


def box_x_compare(a, b):
    return box_compare(a, b, 0)


def box_y_compare(a, b):
    return box_compare(a, b, 1)


def box_z_compare(a, b):
    return box_compare(a, b, 2)


class BoundingVolumeNode(Primitive):

    def __init__(self, obj_list, start=0, end=0) -> None:
        super().__init__(name="bounding_volume_hierarchy")
        self.left_node = None
        self.right_node = None
        self.boundingbox = None
        end = end if end != 0 else len(obj_list)
        self.build_tree(obj_list, start, end)

    def intersect(self, ray, ray_dist_interval):
        if not self.boundingbox.intersect(ray, ray_dist_interval):
            return False, None  # TODO: pass None instead?

        left_isect = self.left_node.intersect(ray, ray_dist_interval)
        interval = Interval(ray_dist_interval.min,
                            left_isect.distance if left_isect is not None else ray_dist_interval.max_dist)
        right_isect = self.right_node.intersect(ray, interval)
        if left_isect is not None:
            return True, left_isect
        elif right_isect is not None:
            return True, right_isect
        return False, None

    def build_tree(self, list, start, end):
        axis = random_int(0, 2)
        comparators = {0: box_x_compare, 1: box_y_compare, 2: box_z_compare}
        comparator = comparators[axis]

        object_span = end - start
        if object_span == 1:
            self.left_node = self.right_node = list[start]
        elif object_span == 2:
            if comparator(list[start], list[start + 1]):
                self.left_node = list[start]
                self.right_node = list[start + 1]
            else:
                self.left_node = list[start + 1]
                self.right_node = list[start]
        else:
            # sort the list
            # list[start:end].sort(key=comparator)
            a = list[start:end]
            b = sorted(a, key=lambda x: x.bounding_box.axis(axis).min_dist)
            mid = start + int(object_span / 2)
            self.left_node = BoundingVolumeNode(b, start, mid)
            self.right_node = BoundingVolumeNode(b, mid, end)

        self.boundingbox = BoundingBox()
        self.boundingbox.from_boundingbox(self.left_node.boundingbox, self.right_node.boundingbox)
