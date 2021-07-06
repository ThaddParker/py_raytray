from utils.interval import Interval


class BoundingBox:

    def __init__(self, intervalx=Interval(), intervaly=Interval(), intervalz=Interval()):

        self.ix = intervalx
        self.iy = intervaly
        self.iz = intervalz

    def from_vectors(self, min_vector, max_vector):
        # two point represent extrema
        self.ix = Interval(min(min_vector[0], max_vector[0]), max(min_vector[0], max_vector[0]))
        self.iy = Interval(min(min_vector[1], max_vector[1]), max(min_vector[1], max_vector[1]))
        self.iz = Interval(min(min_vector[2], max_vector[2]), max(min_vector[2], max_vector[2]))

    def from_boundingbox(self, bbox0, bbox1):
        self.ix = Interval(bbox0.ix, bbox1.ix)
        self.iy = Interval(bbox0.iy, bbox1.iy)
        self.iz = Interval(bbox0.iz, bbox1.iz)

    def intersect(self, ray_in, ray_interval):
        for i in range(3):
            invD = 1. / ray_in.direction[i]
            t0 = min((self.axis(i).min_dist - ray_in.origin[i]) / ray_in.direction[i],
                     (self.axis(i).max_dist - ray_in.origin[i] / ray_in.direction[i]))

            t1 = max((self.axis(i).min_dist - ray_in.origin[i]) / ray_in.direction[i],
                     (self.axis(i).max_dist - ray_in.origin[i] / ray_in.direction[i]))

            ray_interval.min_dist = max(t0.min_dist, ray_interval.min_dist)
            ray_interval.max_dist = min(t1.max_dist, ray_interval.max_dist)
            if ray_interval.max_dist <= ray_interval.min_dist:
                return False
            return True

    def axis(self, n):
        if n == 1:
            return self.iy
        if n == 2:
            return self.iz
        return self.ix

    def __add__(self, offset):
        return BoundingBox(self.ix + offset.x, self.iy + offset.y, self.iz + offset.z)

    def __radd__(self, offset):
        return self + offset
