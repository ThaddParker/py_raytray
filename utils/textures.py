from abc import ABC, abstractmethod
import math

from utils.colors import RGBColor
from utils.perlin import PerlinNoise


class Texture(ABC):

    def __init__(self, name='unnamed_texture'):
        self.name = name

    @abstractmethod
    def value(self, uv_point, point):
        pass


class Pigment(Texture):
    """Pigment represents a solid color to be applied to a surface"""

    def __init__(self, color: RGBColor):
        super().__init__("pigment_color")
        self.color = color  # RGBColor value for this

    def value(self, uv_point, point):
        # point is not used in this case
        return self.color


class Gradient(Texture):
    """A gradient linear interpolate color scheme"""

    def __init__(self, start_color=RGBColor(1.0, 1.0, 1.0), end_color=RGBColor(0.5, 0.7, 1.0), axis=1):
        """Gradient in most likely the x(0) and y(1) axis. """
        super().__init__("gradient_texture")
        self.start_color = start_color if isinstance(start_color, Texture) else Pigment(start_color)
        self.end_color = end_color if isinstance(end_color, Texture) else Pigment(end_color)
        self.axis = axis

    def value(self, uv_point, point):
        unit_dir = point.direction.normalize()
        t = 0.5 * (unit_dir[self.axis] + 1)
        return (1.0 - t) * self.start_color.color + t * self.end_color.color


class Checker(Texture):
    """A checkered pattern whose size between even and odd colors is base on a scale value."""

    def __init__(self, scale, even_color, odd_color):
        super().__init__(name="checker_texture")
        self.scale = scale
        self.inv_scale = 1. / scale
        self.even_color = even_color if isinstance(even_color, Texture) else Pigment(even_color)
        self.odd_color = odd_color if isinstance(odd_color, Texture) else Pigment(odd_color)

    def value(self, uv_point, point):
        x_int = int(math.floor(self.inv_scale * point.x))
        y_int = int(math.floor(self.inv_scale * point.y))
        z_int = int(math.floor(self.inv_scale * point.z))

        even = (x_int + y_int + z_int) % 2 == 0
        return self.even_color.value(uv_point, point) if even else self.odd_color.value(uv_point, point)


class Perlin(Texture):

    def __init__(self, scale, pn=None):
        super().__init__("perlin_texture")
        self.perlin_noise = pn if pn is not None else PerlinNoise()
        self.scale = scale

    def value(self, uv_point, point):
        val = 1. + self.perlin_noise.noise(self.scale * point)
        return RGBColor(1, 1, 1) * 0.5 * val


class Turbulence(Perlin):

    def __init__(self,scale, pn):
        super().__init__(scale, pn)
        self.name = "turbulence_texture"
        self.perlin_noise = pn if pn is not None else PerlinNoise()
        self.scale = scale

    def value(self, uv_point, point):
        s = self.scale * point
        return RGBColor(1,1,1) * self.perlin_noise.turbulence(s)

class Marble(Perlin):
    def __init__(self,scale, pn):
        super().__init__(scale, pn)
        self.name = "turbulence_texture"
        self.perlin_noise = pn if pn is not None else PerlinNoise()
        self.scale = scale

    def value(self, uv_point, point):
        s = self.scale * point
        return RGBColor(1,1,1) * 0.5 * (1. + math.sin(s.z + 10 * self.perlin_noise.turbulence(s)))