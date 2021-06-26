

class Ray:
    """A basic ray object"""
    
    def __init__(self, origin, direction) -> None:
        self.origin = origin
        self.direction = direction
        
    def evaluate(self, t):
        return self.origin + t * self.direction