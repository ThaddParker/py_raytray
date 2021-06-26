import math


class Interval:

    def __init__(self, min_dist=-math.inf, max_dist= math.inf):
        self.min_dist = min_dist
        self.max_dist = max_dist

    def contains(self, x):
        return self.min_dist <= x <= self.max_dist

    def clamp(self, x):
        if x < self.min_dist:
            return self.min_dist
        if x > self.max_dist:
            return self.max_dist
        return x

empty = Interval(math.inf, -math.inf)
universe = Interval(-math.inf, math.inf)


