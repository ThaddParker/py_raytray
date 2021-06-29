import math

from utils.colors import RGBColor
from utils.functs import random_double
from utils.image import Image
from tqdm import tqdm

from utils.interval import Interval
from utils.textures import Gradient, Pigment


class Scene:
    def __init__(self,scene_settings, primitive_list, camera):
        self.scene_settings = scene_settings
        self.image = Image(scene_settings.image_width)
        self.camera = camera
        self.objects = primitive_list

    def render(self):
        with open(self.scene_settings.image_file_name, "w") as img_file:
            img_file.write("P3 {} {}\n255\n".format(self.image.width, self.image.height))
            for j in tqdm(reversed(range(self.image.height))):
                for i in range(self.image.width):
                    pixel_color = RGBColor(0, 0, 0)
                    for s in range(self.scene_settings.samplesperpixel):
                        x = float(i + random_double()) / self.image.width
                        y = float(j + random_double()) / self.image.height
                        ray = self.camera.create_ray(x, y)
                        pixel_color += self.ray_color(ray, self.scene_settings.max_depth)  # RGBColor(float(i)/image.width, float(j)/image.height, 0.25)
                        # image.set_pixel(i, j, pixel_color)

                    self.write_color(img_file, pixel_color, self.scene_settings.samplesperpixel)
                    # img_file.write(
                    #     "{} {} {} ".format(to_byte(pixel_color.red), to_byte(pixel_color.green), to_byte(pixel_color.blue)))
                img_file.write("\n")

    def ray_color(self, ray,  depth):
        if depth <= 0:
            return RGBColor(0, 0, 0)

        isect = self.objects.intersect(ray, Interval(0.001, math.inf))

        if isect is not None:
            good, ray_scattered, attenuation = isect.material.scatter(ray, isect)
            if good:
                ray = ray_scattered
                return attenuation * self.ray_color(ray, depth - 1)
            else:
                return RGBColor(0, 0, 0) # black

            # vec = 0.5 * (isect.normal + Vector3(1, 1, 1))
            # target = isect.point + random_in_hemisphere(isect.normal) # +  isect.normal + random_unit_vector() # random_in_unit_sphere()
            # val = 0.5 * ray_color(Ray(isect.point, target - isect.point), scene, depth - 1)
            # return val  #  RGBColor(vec.x, vec.y, vec.z)

            # dist = sphere_intersect(Vector3(0, 0, -1), 0.5, ray)
            # if dist > 0.0:
            #     n = (ray.evaluate(dist) - Vector3(0,0,-1)).normalize()
            #     return 0.5 * RGBColor(n.x + 1, n.y + 1, n.z + 1)
        # else:
            # this will be the skysphere with atmospherics
        background = Gradient(Pigment(RGBColor(1.0, 1.0, 1.0)), Pigment(RGBColor(0.5, 0.7, 1.0)))
        return background.value((0, 0), ray)
            # gradient texture
            # unit_dir = ray.direction.normalize()
            # t = 0.5 * (unit_dir.y + 1)
            # return (1.0 - t) * RGBColor(1.0, 1.0, 1.0) + t * RGBColor(0.5, 0.7, 1.0)

    def write_color(self, image_file, pixel_color, samples_per_pixel):
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