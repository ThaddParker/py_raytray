from abc import ABC


class Texture(ABC):

    def __init__(self, name='unnamed_texture'):
        self.name = name


class Pigment(Texture):
    """Pigment represents a singular color to be applied to a surface"""

    def __init__(self, color):
        super().__init__("pigment_color")
        self.color = color  # RGBColor value for this


class Gradient(Texture):

    def __init__(self, start_color, end_color, axis):
        """Gradient in most likely the x and y axis. """
        super().__init__("gradient_texture")
        self.start_color = start_color
        self.end_color = end_color
        self.axis = axis
