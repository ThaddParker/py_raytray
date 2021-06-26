from abc import ABC, abstractmethod


class Texture(ABC):

    def __init__(self, name='unnamed_texture'):
        self.name = name

    @abstractmethod
    def value(self, point):
        pass


class Pigment(Texture):
    """Pigment represents a singular color to be applied to a surface"""

    def __init__(self, color):
        super().__init__("pigment_color")
        self.color = color  # RGBColor value for this

    def value(self, point):
        # point is not used in this case
        return self.color


class Gradient(Texture):

    def __init__(self, start_color: Pigment, end_color: Pigment, axis):
        """Gradient in most likely the x and y axis. """
        super().__init__("gradient_texture")
        self.start_color = start_color
        self.end_color = end_color
        self.axis = axis

    def value(self, point):
        pass  # TODO: need to work with this formula
