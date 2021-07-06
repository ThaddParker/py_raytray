import math
from abc import ABC

from utils.functs import reflect, random_in_unit_sphere, refract, near_zero, random_double
from utils.ray import Ray
from utils.textures import Pigment, Texture
from utils.colors import RGBColor


class Material(ABC):

    def __init__(self, name='base_material'):
        self.name = name

    def emit(self, uv_coord, point):
        return RGBColor(0, 0, 0)  # returns a black color

    def scatter(self, ray_in, isect):
        pass


class Diffuse(Material):

    def __init__(self, color):
        super().__init__("diffuse_material")
        if isinstance(color, Texture):
            self.pigment = color
        else:
            # assuming an RGBColor
            self.pigment = Pigment(color)

    def __str__(self):
        return self.name + ":pigment: %s" % self.pigment.color.__str__()

    def scatter(self, ray_in, isect):
        scatter_dir = isect.normal + random_in_unit_sphere()
        # catch degenerate scatter direction
        if near_zero(scatter_dir):
            scatter_dir = isect.normal
        scattered = Ray(isect.point, scatter_dir, ray_in.time)
        attenuation = self.pigment.value(isect.uv_coordinates, isect.point)
        return True, scattered, attenuation


class Metal(Material):

    def __init__(self, color, roughness):
        super().__init__("metallic_material")
        if isinstance(color, Texture):
            self.pigment = color
        else:
            # assuming an RGBColor
            self.pigment = Pigment(color)
        self.roughness = roughness if roughness < 1. else 1.
        self.shininess = None

    def __str__(self):
        return self.name + ":pigment: %s" % self.pigment.color.__str__()

    def scatter(self, ray_in, isect):
        reflected = reflect(ray_in.direction.normalize(), isect.normal)
        ray_scattered = Ray(isect.point, reflected + self.roughness * random_in_unit_sphere(), ray_in.time)
        attenuation = self.pigment.color
        d = ray_scattered.direction.dot(isect.normal) > 0
        return d, ray_scattered, attenuation


class Refractive(Material):

    def __init__(self, color, ior):
        super().__init__("refractive_material")
        if isinstance(color, Texture):
            self.pigment = color
        else:
            # assuming an RGBColor
            self.pigment = Pigment(color)
        self.ior = ior

    def __str__(self):
        return self.name + ":pigment: %s" % self.pigment.color.__str__()

    def scatter(self, ray_in, isect):
        attenuation = RGBColor(1, 1, 1)  # TODO: use the internal pigment so that you can have different colors of glass
        refraction_ratio = 1. / self.ior if isect.front_face else self.ior
        unit_direction = ray_in.direction.normalize()
        cos_theta = min(-unit_direction.dot(isect.normal), 1.0)
        sin_theta = math.sqrt(1. - cos_theta * cos_theta)
        cannot_refract = refraction_ratio * sin_theta > 1.
        # direction = None
        if (cannot_refract or self.reflectance(cos_theta, refraction_ratio)) > random_double():
            direction = reflect(unit_direction, isect.normal)
        else:
            direction = refract(unit_direction, isect.normal, refraction_ratio)

        scattered_ray = Ray(isect.point, direction, ray_in.time)
        return True, scattered_ray, attenuation

    @staticmethod
    def reflectance(cosine, refractive_index):
        # use schlick's approximation
        r0 = (1. - refractive_index) / (1. + refractive_index)
        r0 = r0 * r0
        return r0 + (1. - r0) * math.pow(1. - cosine, 5)


class Checkered(Material):

    def __init__(self, scale, even_color=Pigment(RGBColor(1, 1, 1)), odd_color=Pigment(RGBColor(0, 0, 0))):
        super().__init__("checkered_material")
        self.scale = scale
        self.even_color = even_color
        self.odd_color = odd_color

    def __str__(self):
        return self.name + ":evenpigment: {}: oddpigment {}".format(self.even_color.__str__(), self.odd_color.__str__())

    def scatter(self, ray_in, isect):
        pass
