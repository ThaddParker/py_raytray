import math


class Interval:

    def __init__(self, min_dist=-math.inf, max_dist=math.inf):
        self.min_dist = min_dist
        self.max_dist = max_dist

    def __str__(self):
        return "{:.4f}, {:.4f}".format(self.min_dist, self.max_dist)

    def __repr__(self) -> str:
        return "Interval: {:.4f}, {:.4f}".format(self.min_dist, self.max_dist)

    def contains(self, x):
        return self.min_dist <= x <= self.max_dist

    def clamp(self, x):
        if x < self.min_dist:
            return self.min_dist
        if x > self.max_dist:
            return self.max_dist
        return x

    def __add__(self, displacement):
        return Interval(self.min_dist + displacement, self.max_dist + displacement)

    def __radd__(self, displacement):
        return self + displacement

    def __sub__(self, displacement):
        return Interval(self.min_dist - displacement, self.max_dist - displacement)

    def __rsub__(self, displacement):
        return self - displacement

    def __div__(self, val):
        return Interval(self.min_dist / val, self.max_dist / val)

    def __truediv__(self, val):
        return Interval(self.min_dist / val, self.max_dist / val)

    def __lt__(self, other):
        if isinstance(other, Interval):
            return self.min_dist < other.min_dist and self.max_dist < other.max_dist
        else:
            return self.min_dist < other and self.max_dist < other


empty = Interval(math.inf, -math.inf)
universe = Interval(-math.inf, math.inf)
