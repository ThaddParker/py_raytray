from abc import abstractmethod, ABC

from utils.functs import random_unit_vector
from utils.ray import Ray
from utils.textures import Pigment, Texture
from utils.colors import RGBColor


class Material(ABC):

    def __init__(self, name='base_material'):
        self.name = name

    @abstractmethod
    def scatter(self, ray_in, isect, color, ray_scattered):
        pass


class Diffuse(Material):

    def __init__(self, color):
        super().__init__("diffuse_material")
        if isinstance(color, Texture):
            self.pigment = color
        else:
            # assuming an RGBColor
            self.pigment = Pigment(color)

    def scatter(self, ray_in, isect, color, ray_scattered):
        scatter_dir = isect.normal + random_unit_vector()
        scattered = Ray(isect.point, scatter_dir)
        attenuation = color.color
        return scattered, attenuation


class Checkered(Material):

    def __init__(self, even_color=RGBColor(1, 1, 1), odd_color=RGBColor(0, 0, 0)):
        super().__init__("checkered_material")
        self.even_color = even_color
        self.odd_color = odd_color

    def scatter(self, ray_in, isect, color, ray_scattered):
        pass
