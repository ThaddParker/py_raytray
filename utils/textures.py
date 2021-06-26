from abc import ABC, abstractmethod

from utils.colors import RGBColor


class Texture(ABC):

    def __init__(self, name='unnamed_texture'):
        self.name = name

    @abstractmethod
    def value(self, point, ray):
        pass


class Pigment(Texture):
    """Pigment represents a singular color to be applied to a surface"""

    def __init__(self, color):
        super().__init__("pigment_color")
        self.color = color  # RGBColor value for this

    def value(self, point, ray):
        # point is not used in this case
        return self.color


class Gradient(Texture):

    def __init__(self, start_color=Pigment(RGBColor(1.0, 1.0, 1.0)), end_color=Pigment(RGBColor(0.5, 0.7, 1.0)), axis=1):
        """Gradient in most likely the x and y axis. """
        super().__init__("gradient_texture")
        self.start_color = start_color
        self.end_color = end_color
        self.axis = axis

    def value(self, point, ray):
        unit_dir = ray.direction.normalize()
        t = 0.5 * (unit_dir[self.axis] + 1)
        return (1.0 - t) * self.start_color.color + t * self.end_color.color
