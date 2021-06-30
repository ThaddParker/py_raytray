from utils.camera import Camera
from utils.functs import random_double, random_in_unit_sphere, random_unit_vector, random_in_hemisphere
from utils.image import Image
from utils.colors import RGBColor
from utils.interval import Interval
from utils.materials import Diffuse, Metal
from utils.primitive_list import PrimitiveList
from utils.scene import Scene
from utils.scene_settings import SceneSettings
from utils.shapes import Sphere
from utils.textures import Pigment
import time
from tqdm import tqdm
from vectormath import Vector3
import math


# def sphere_intersect(center, radius, ray):
#     oc = ray.origin - center
#     a = ray.direction.dot(ray.direction)
#     half_b = ray.direction.dot(oc) #2.0 * oc.dot(ray.direction)
#     c = oc.dot(oc) - radius**2
#     disc = half_b**2 - a*c
#
#     if disc < 0:
#         return -1.0
#     else:
#         return (-half_b - math.sqrt(disc)) /(a)


# def ray_color(ray, scene, depth):
#     if depth <= 0:
#         return RGBColor(0, 0, 0)
#
#     isect = scene.intersect(ray, Interval(0.001, math.inf))
#
#     if isect is not None:
#         good, ray_scattered, attenuation = isect.material.scatter(ray, isect)
#         if good:
#             return attenuation * ray_color(ray, scene, depth - 1)
#         else:
#             return RGBColor(0, 0, 0)
#
#         # vec = 0.5 * (isect.normal + Vector3(1, 1, 1))
#         # target = isect.point + random_in_hemisphere(isect.normal) # +  isect.normal + random_unit_vector() # random_in_unit_sphere()
#         # val = 0.5 * ray_color(Ray(isect.point, target - isect.point), scene, depth - 1)
#         # return val  #  RGBColor(vec.x, vec.y, vec.z)
#
#     # dist = sphere_intersect(Vector3(0, 0, -1), 0.5, ray)
#     # if dist > 0.0:
#     #     n = (ray.evaluate(dist) - Vector3(0,0,-1)).normalize()
#     #     return 0.5 * RGBColor(n.x + 1, n.y + 1, n.z + 1)
#
#     # gradient texture
#     unit_dir = ray.direction.normalize()
#     t = 0.5 * (unit_dir.y + 1)
#     return (1.0 - t) * RGBColor(1.0, 1.0, 1.0) + t * RGBColor(0.5, 0.7, 1.0)
#
#
# def write_color(image_file, pixel_color, samples_per_pixel):
#     # get the color values locally
#     r = pixel_color.red
#     g = pixel_color.green
#     b = pixel_color.blue
#
#     # do the gamma correction
#     scale = 1. / samples_per_pixel
#     r = math.sqrt(scale * r)
#     g = math.sqrt(scale * g)
#     b = math.sqrt(scale * b)
#
#     # clamp values to [0..1]
#     intensity = Interval(0.000, 0.999)
#     ri = int(256 * intensity.clamp(r))
#     gi = int(256 * intensity.clamp(g))
#     bi = int(256 * intensity.clamp(b))
#
#     image_file.write("{} {} {} ".format(ri, gi, bi))


def main():
    print("ok")
    settings = SceneSettings(20, 5, (16./9.))
    settings.image_width = 1200



    # samplesperpixel = 100
    # maxdepth = 50
    # image = Image(400)
    camera = Camera(Vector3(13,2,3),Vector3(0,0,0), settings.aspect_ratio)
    camera.vup = Vector3(0,1,0)
    camera.vertical_fov = 90
    camera.aperture = 0.1

    camera.focus_distance = (camera.origin - camera.look_at).length
    camera.initialize_camera()
    # camera.vertical_fov = 20
    t0 = time.time()
    sceneobjs = PrimitiveList()

    matground = Diffuse(RGBColor(0.8, 0.8, 0))
    matcenter = Diffuse(RGBColor(0.7, 0.3, 0.3))
    matleft = Metal(RGBColor(0.8, 0.8, 0.8), 0.3)
    matright = Metal(RGBColor(0.8, 0.6, 0.2), 1.0)

    sceneobjs.add(Sphere(Vector3(0, 0, -1), 1, matcenter))
    sceneobjs.add(Sphere(Vector3(0, -1000.5, -1), 1000, matground))
    # sceneobjs.add(Sphere(Vector3(-1, 0, -1), 0.5, matleft))
    # sceneobjs.add(Sphere(Vector3(1, 0, -1), 0.5, matright))
    scene = Scene(settings, sceneobjs, camera)

    scene.render()
    # def to_byte(color_item):
    #     return round(max(min(color_item * 255, 255), 0))

    # with open("first_test.ppm", "w") as img_file:
    #     img_file.write("P3 {} {}\n255\n".format(image.width, image.height))
    #     for j in tqdm(reversed(range(image.height))):
    #         for i in range(image.width):
    #             pixel_color = RGBColor(0, 0, 0)
    #             for s in range(scene.scene_settings.samplesperpixel):
    #                 x = float(i + random_double()) / image.width
    #                 y = float(j + random_double()) / image.height
    #                 ray = camera.create_ray(x, y)
    #                 pixel_color += ray_color(ray, sceneobjs,
    #                                          scene.scene_settings.max_depth)  # RGBColor(float(i)/image.width, float(j)/image.height, 0.25)
    #                 # image.set_pixel(i, j, pixel_color)
    #
    #             write_color(img_file, pixel_color, scene.scene_settings.samplesperpixel)
    #             # img_file.write(
    #             #     "{} {} {} ".format(to_byte(pixel_color.red), to_byte(pixel_color.green), to_byte(pixel_color.blue)))
    #         img_file.write("\n")
    # # with open("first_test.ppm", "w") as img_file:
    # #     image.write_ppm_file(img_file)
    t1 = time.time()
    diff = t1 - t0
    print("Done...\nTime: %s seconds" % diff)


if __name__ == "__main__":
    main()
