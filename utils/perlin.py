from vectormath import Vector3

from utils.functs import random_double, random_int, random_vector
import math
import numpy as np


class PerlinNoise:

    def __init__(self) -> None:
        self.point_count = 257
        self.rand_float = [0.] * (self.point_count + self.point_count)
        self.rand_vector = [Vector3()] * (self.point_count + self.point_count)
        for i in range(self.point_count):
            self.rand_vector[i] = (random_vector(-1., 1.)).normalize()

        for i in range(self.point_count):
            self.rand_float[i] = random_double()

        self.permute_x = self._generate_permutation()
        self.permute_y = self._generate_permutation()
        self.permute_z = self._generate_permutation()

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
                        self.permute_x[i + di] ^ self.permute_y[j + dj] ^ self.permute_z[k + dk]
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

    def vectornoise(self, point):
        u = point.x - math.floor(point.x)
        v = point.y - math.floor(point.y)
        w = point.z - math.floor(point.z)

        i = int(4 * point.x) & 255
        j = int(4 * point.y) & 255
        k = int(4 * point.z) & 255

        c = np.full_like((2, 2, 2), dtype=Vector3)
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di, dj, dk] = self.rand_vector[
                        self.permute_x[i + di] ^ self.permute_y[j + dj] ^ self.permute_z[k + dk]
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
                for k in range(3):
                    weight_v = Vector3(u - i, v - j, w - k)
                    accumulation += (i * uu + (1 - i) * (1 - uu)) *\
                              (j * vv + (1 - j) * (1 - vv)) *\
                              (k * ww + (1 - k) * (1 - ww)) *\
                              (c[i, j, k]).dot(weight_v)

        return accumulation

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
