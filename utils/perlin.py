from vectormath import Vector3

from utils.functs import random_double, random_int, random_vector, smooth_step
import math
import numpy as np
from random import shuffle


class PerlinNoise:

    def __init__(self) -> None:
        self.point_count = 256
        self.point_count_mask = self.point_count - 1
        # version 1 & 2 -- possibly not good?
        self.rand_float = [0.] * self.point_count
        self.rand_vector = [Vector3()] * self.point_count
        for i in range(self.point_count):
            self.rand_vector[i] = (random_vector(-1., 1.)).normalize()

        for i in range(self.point_count):
            self.rand_float[i] = random_double()

        self.permute_x = self._generate_permutation()
        self.permute_y = self._generate_permutation()
        self.permute_z = self._generate_permutation()
        # version 3
        self.temp_table = []
        self.r = []
        for i in range(self.point_count):
            self.r.append(random_vector(-1., 1.))
            self.temp_table.append(i)

        shuffle(self.temp_table)
        self.permute_x_table = self.temp_table + self.temp_table
        shuffle(self.temp_table)
        self.permute_y_table = self.temp_table + self.temp_table
        shuffle(self.temp_table)
        self.permute_z_table = self.temp_table + self.temp_table

    def evaluate(self, vector):
        i = math.floor(vector.x)
        j = math.floor(vector.y)
        k = math.floor(vector.z)
        u = vector.x - i
        v = vector.y - j
        w = vector.z - k

        su = smooth_step(u)
        sv = smooth_step(v)
        sw = smooth_step(w)

        c = [Vector3()] * 8
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    idx = self.permute_x_table[(i + di) & 255] ^ self.permute_y_table[(j + dj) & 255] ^ \
                          self.permute_z_table[
                              (k + dk) & 255]
                    val = self.r[idx]
                    idx = di * 4 + dj * 2 + dk
                    c[idx] = val

        return self.perlin_interpolate(c, su, sv, sw)

    def perlin_interpolate(self, c, u: float, v: float, w: float) -> float:
        accum = 0.0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = Vector3(u - i, v - j, w - k)
                    weight = (c[i * 4 + j * 2 + k]).dot(weight_v)
                    accum += (i * u + (1 - i) * (1 - u)) * (j * v + (1 - j) * (1 - v)) * (
                            k * w + (1 - k) * (1 - w)) * weight

        return accum

    def noise(self, point):
        u = point.x - math.floor(point.x)
        v = point.y - math.floor(point.y)
        w = point.z - math.floor(point.z)

        i = int(4 * point.x) & 255
        j = int(4 * point.y) & 255
        k = int(4 * point.z) & 255

        u = u * u * (3. - 2. * u)
        v = v * v * (3. - 2. * v)
        w = w * w * (3. - 2. * w)

        c = np.zeros((2, 2, 2))
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di, dj, dk] = self.rand_float[
                        self.permute_x[(i + di) & 255] ^ self.permute_y[(j + dj) & 255] ^ self.permute_z[(k + dk) & 255]
                        ]

        return self.trilinear_interpolation(c, u, v, w)

    @staticmethod
    def trilinear_interpolation(c, u, v, w):
        accumulation = 0.
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    accumulation += (i * u + (1 - i) * (1 - u)) * \
                                    (j * v + (1 - j) * (1 - v)) * \
                                    (k * w + (1 - k) * (1 - w)) * c[i, j, k]
        return accumulation

    def vector_noise(self, point):
        u = point.x - math.floor(point.x)
        v = point.y - math.floor(point.y)
        w = point.z - math.floor(point.z)

        i = int(4 * point.x) & 255
        j = int(4 * point.y) & 255
        k = int(4 * point.z) & 255

        # c = np.full_like((2, 2, 2), fill_value=Vector3(), dtype= Vector3)
        c = np.ndarray((2, 2, 2), dtype=Vector3)
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di, dj, dk] = self.rand_vector[
                        self.permute_x[(i + di) & 255] ^ self.permute_y[(j + dj) & 255] ^ self.permute_z[(k + dk) & 255]
                        ]

        return self.interpolate(c, u, v, w)

    @staticmethod
    def interpolate(c, u, v, w):
        uu = u * u * (3. - 2. * u)
        vv = v * v * (3. - 2. * v)
        ww = w * w * (3. - 2. * w)
        accumulation = 0.0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = Vector3(u - i, v - j, w - k)
                    accumulation += (i * uu + (1 - i) * (1 - uu)) * \
                                    (j * vv + (1 - j) * (1 - vv)) * \
                                    (k * ww + (1 - k) * (1 - ww)) * \
                                    (c[i, j, k]).dot(weight_v)

        return accumulation

    def turbulence(self, point, depth=7):
        accumulation = 0.
        temp_point = point
        weight = 1.
        for i in range(depth):
            accumulation += weight * self.vector_noise(temp_point)
            weight *= 0.5
            temp_point *= 2

        return math.fabs(accumulation)

    def _generate_permutation(self):
        p = [0] * self.point_count
        for i in range(self.point_count):
            p[i] = i
        p = self._permute(p, self.point_count)
        return p

    @staticmethod
    def _permute(p, n):
        for i in reversed(range(n)):
            target = random_int(0, i)
            tmp = p[i]
            p[i] = p[target]
            p[target] = tmp
        return p
