from typing import Optional
import math
from utils.boundingbox import BoundingBox

from vectormath.vector import Vector3
from utils.primitive_list import PrimitiveList

from utils.intersection import Intersection
from utils.interval import Interval
from utils.shapes import Primitive
from utils.functs import random_int

def box_compare(a:Primitive, b:Primitive, axis):
    return a.boundingbox.axis(axis).min_dist < b.boundingbox.axis(axis).min_dist
def box_x_compare(a, b):
    return box_compare(a,b, 0)
    # returns x component of the Geometry (or other Hittable)... used for list sorting key
    # box = a.boundingbox # (time0, time1)
    # return box.vmin.ix

def box_y_compare(a, b):
    return box_compare(a, b, 1)
    # returns y component of the Geometry (or other Hittable)... used for list sorting key
    # box = a.boundingbox(time0, time1)
    # return box.vmin.iy

def box_z_compare(a, b):
    return box_compare(a, b, 2)

    # returns z component of the Geometry (or other Hittable)... used for list sorting key
    # box = a.boundingbox(time0, time1)
    # return box.vmin.iz

def surrounding_box(box1: BoundingBox, box2: BoundingBox) -> BoundingBox:
    # return the bounding box surrounding two bounding boxes (i.e. the union)
    if box1 is None:
        return box2
    if box2 is None:
        return box1

    b1_min = box1.vmin
    b2_min = box2.vmin
    b1_max = box1.vmax
    b2_max = box2.vmax

    new_x_min = min(b1_min.x, b2_min.x)
    new_y_min = min(b1_min.y, b2_min.y)
    new_z_min = min(b1_min.z, b2_min.z)
    new_min = Vector3(new_x_min, new_y_min, new_z_min)

    new_x_max = max(b1_max.x, b2_max.x)
    new_y_max = max(b1_max.y, b2_max.y)
    new_z_max = max(b1_max.z, b2_max.z)
    new_max = Vector3(new_x_max, new_y_max, new_z_max)
    new_box = BoundingBox()
    new_box.from_vectors(new_min, new_max)
    return new_box

class BoundingVolumeNode(Primitive):

    def __init__(self, obj_list,start=0,end=0) -> None:
        super().__init__(name="bounding_volume_hierarchy")
        self.left_node = None
        self.right_node = None
        self.boundingbox = None
        end= end if end != 0 else len(obj_list)
        self.build_tree(obj_list, start, end)


    def intersect(self, ray, ray_dist_interval) -> Optional[Intersection]:
        if not self.boundingbox.intersect(ray, ray_dist_interval):
            return False, None # TODO: pass None instead?

        left_isect = self.left_node.intersect(ray, ray_dist_interval)
        interval = Interval(ray_dist_interval.min, left_isect.distance if left_isect is not None else ray_dist_interval.max_dist)
        right_isect = self.right_node.intersect(ray, interval)
        if left_isect is not None:
            return True, left_isect
        elif right_isect is not None:
            return True, right_isect
        return False, None

    def build_tree(self, list, start, end):
        axis = random_int(0,2)
        comparators = {0: box_x_compare, 1: box_y_compare, 2: box_z_compare}
        comparator = comparators[axis]

        object_span = end - start
        if (object_span == 1):
            self.left_node = self.right_node = list[start]
        elif (object_span == 2):
            if (comparator(list[start], list[start+1])):
                self.left_node = list[start]
                self.right_node = list[start+1]
            else:
                self.left_node = list[start+1]
                self.right_node = list[start]
        else:
            #sort the list
            # list[start:end].sort(key=comparator)
            a = list[start:end]
            b = sorted(a, key=lambda x:x.boundingbox.axis(axis).min_dist)
            mid = start + int(object_span/2)
            self.left_node = BoundingVolumeNode(b,start, mid)
            self.right_node = BoundingVolumeNode(b,mid, end)
        
        self.boundingbox = BoundingBox()
        self.boundingbox.from_boundingbox(self.left_node.boundingbox, self.right_node.boundingbox)
        
        # no_bbox_list = list.no_has_bbox_list()
        # has_bbox_list = list.has_bbox_list()

        # if len(no_bbox_list) != 0:
        #     vmin = Vector3(-math.inf, -math.inf, -math.inf)
        #     vmax = Vector3(math.inf, math.inf, math.inf)
        #     self.bbox = BoundingBox(vmin, vmax)

        #     if len(has_bbox_list) == 0:
        #         if len(no_bbox_list) == 1:
        #             self.left = no_bbox_list[0]
        #             self.right = None
        #         elif len(no_bbox_list) == 2:
        #             self.left = no_bbox_list[0]
        #             self.right = no_bbox_list[1]
        #         else:
        #             mid = len(no_bbox_list) // 2
        #             geom_list = PrimitiveList(no_bbox_list[:mid])
        #             self.left = BoundingVolumeNode(geom_list, time0, time1)
        #             geom_list = PrimitiveList(no_bbox_list[mid:])
        #             self.right = BoundingVolumeNode(geom_list, time0, time1)
        #     else:  # len(has_bbox_list) != 0
        #         if len(no_bbox_list) == 1:
        #             self.left = no_bbox_list[0]
        #         else:
        #             geom_list = PrimitiveList(no_bbox_list)
        #             self.left = BoundingVolumeNode(geom_list, time0, time1)

        #         if len(has_bbox_list) == 1:
        #             self.right = has_bbox_list[0]
        #         else:
        #             geom_list = PrimitiveList(has_bbox_list)
        #             self.right = BoundingVolumeNode(geom_list, time0, time1)
        # else:  # len(no_bbox_list) == 0
        #     if len(has_bbox_list) > 1:
        #         axis = random_int(0,2)
        #         comparators = {0: box_x_compare, 1: box_y_compare, 2: box_z_compare}
        #         comparator = comparators[axis]

        #     if len(has_bbox_list) == 1:
        #         self.left = has_bbox_list[0]
        #         self.right = None
        #     elif len(has_bbox_list) == 2:
        #         obj0 = has_bbox_list[0]
        #         obj1 = has_bbox_list[1]

        #         if comparator(obj0) < comparator(obj1):
        #             self.left = obj0
        #             self.right = obj1
        #         else:
        #             self.left = obj1
        #             self.right = obj0
        #     else:
        #         has_bbox_list.sort(key=comparator)
        #         mid = len(has_bbox_list) // 2
        #         geom_list_left = PrimitiveList(has_bbox_list[:mid])
        #         self.left = BoundingVolumeNode(geom_list_left, time0, time1)
        #         geom_list_right = PrimitiveList(has_bbox_list[mid:])
        #         self.right = BoundingVolumeNode(geom_list_right, time0, time1)

        #     right_bbox = None
        #     left_bbox = self.left.bounding_box(time0, time1)
        #     if self.right is not None:
        #         right_bbox = self.right.bounding_box(time0, time1)

        #     self.bbox = surrounding_box(left_bbox, right_bbox)
