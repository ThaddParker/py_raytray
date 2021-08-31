import math

from utils.colors import RGBColor
from utils.functs import random_double
from utils.image import Image
from tqdm import tqdm

from utils.interval import Interval
from utils.textures import Gradient, Pigment


class Scene:
    def __init__(self, scene_settings, primitive_list, camera):
        self.scene_settings = scene_settings
        self.image = Image(scene_settings.image_width)
        self.camera = camera
        self.objects = primitive_list
        self.background = Gradient(Pigment(RGBColor(1.0, 1.0, 1.0)), Pigment(RGBColor(0.5, 0.7, 1.0)))
        self.ambient = RGBColor(0.5, 0.5, 0.5)

    def render(self):
        print("filename: {}".format(self.scene_settings.image_file_name))
        print("image_width: {} image_height: {}".format(self.image.width, self.image.height))
        with open(self.scene_settings.image_file_name, "w") as img_file:
            img_file.write("P3 {} {}\n255\n".format(self.image.width, self.image.height))
            for j in tqdm(reversed(range(self.image.height))):
                for i in range(self.image.width):
                    pixel_color = RGBColor(0, 0, 0)
                    for s in range(self.scene_settings.samplesperpixel):
                        x = float(i + random_double()) / self.image.width
                        y = float(j + random_double()) / self.image.height
                        ray = self.camera.create_ray(x, y)
                        pixel_color += self.ray_color(ray, self.scene_settings.max_depth)

                    self.write_color(img_file, pixel_color, self.scene_settings.samplesperpixel)

                img_file.write("\n")

    def ray_color(self, ray, depth):
        if depth <= 0:
            return RGBColor(0, 0, 0)

        isect = self.objects.intersect(ray, Interval(0.001, math.inf))
        if isect is None:
            # this will be the skysphere with atmospherics
            return self.background.value((0, 0), ray)

        good, ray_scattered, attenuation = isect.material.scatter(ray, isect)
        emitted = isect.material.emit(isect.uv_coordinates, isect.point)

        if not good:
            return emitted  # this will typically be a black, but could change to ambient or other color base
        else:
            return emitted + attenuation * self.ray_color(ray_scattered, depth - 1)

    @staticmethod
    def write_color(image_file, pixel_color, samples_per_pixel):
        # get the color values locally
        r = pixel_color.red
        g = pixel_color.green
        b = pixel_color.blue

        # do the gamma correction
        scale = 1. / samples_per_pixel
        r = math.sqrt(scale * r)
        g = math.sqrt(scale * g)
        b = math.sqrt(scale * b)

        # clamp values to [0..1]
        intensity = Interval(0.000, 0.999)
        ri = int(256 * intensity.clamp(r))
        gi = int(256 * intensity.clamp(g))
        bi = int(256 * intensity.clamp(b))

        image_file.write("{} {} {} ".format(ri, gi, bi))
