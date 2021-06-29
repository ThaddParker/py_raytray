

class Ray:
    """A basic ray object"""
    
    def __init__(self, origin, direction) -> None:
        self.origin = origin
        self.direction = direction
        
    def evaluate(self, t):
        return self.origin + t * self.direction

    def __str__(self):
        return "origin:{}, direction: {}".format(self.origin.__str__(),self.direction.__str__())

    def __repr__(self):
        return "Ray origin: {}, direction: {}".format(self.origin.__str__(),self.direction.__str__())