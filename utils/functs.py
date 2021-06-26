import math
import random
import numpy as np
from vectormath import Vector3


MTG_19937gen = np.random.Generator(np.random.MT19937(555))


def degrees_to_radians(degrees):
    return degrees * math.pi / 180.


def random_double(minval=0.0, maxval=1.0):
    return MTG_19937gen.uniform(minval, maxval)


def random_int(minval=0, maxval=1):
    return int(random_double(minval, maxval))


def clamp(val, min_val, max_val):
    if val < min_val:
        return min_val
    if val > max_val:
        return max_val
    return val


def random_vector(minval=0.0, maxval=1.0):
    return Vector3(random_double(minval, maxval), random_double(minval, maxval), random_double(minval, maxval))


def random_in_unit_disk():
    while True:
        p = Vector3(random_double(-1, 1), random_double(-1, 1), 0)
        if p.length ** 2 >= 1.0:
            continue
        return p


def random_in_unit_sphere():
    while True:
        p = random_vector(-1., 1.)
        if p.length ** 2 >= 1.0:
            continue
        return p


def random_unit_vector():
    return random_in_unit_sphere().normalize()


def random_in_hemisphere(normal: Vector3):
    in_unit_sphere = random_in_unit_sphere()
    if in_unit_sphere.dot(normal) > 0.0:
        return in_unit_sphere
    else:
        return -in_unit_sphere


def near_zero(vector: Vector3):
    s = 1e-8
    return math.fabs(vector.x) < s and math.fabs(vector.y) < s and math.fabs(vector.z) < s
