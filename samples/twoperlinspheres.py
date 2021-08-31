import time

from utils.camera import Camera
from utils.materials import Diffuse
from utils.perlin import PerlinNoise
from utils.scene import Scene
from utils.scene_settings import SceneSettings
from utils.shapes import Sphere, PrimitiveList
from utils.textures import Perlin, Turbulence, Marble
from vectormath import Vector3


def two_perlin_spheres():

    objects = PrimitiveList()

    perlin_texture = Perlin(4)
    turbulencetxt = Turbulence(2, PerlinNoise())
    marbletxt = Marble(4, PerlinNoise())

    objects.add(Sphere(Vector3(0, -1000, 0), 1000, Diffuse(perlin_texture)))
    objects.add(Sphere(Vector3(0, 2, 0), 2, Diffuse(turbulencetxt)))
    objects.add(Sphere(Vector3(-3, 2, -10), 2, Diffuse(marbletxt)))

    return objects


def build_scene():
    settings = SceneSettings(400, 5, 16 / 9, 400)
    camera = Camera(Vector3(13, 5, 15), Vector3(5, 0, 0), settings.aspect_ratio)
    settings.image_file_name = "twoturbulenceperlinspheres.ppm"
    camera.aperture = 0.
    camera.vup = Vector3(0, 1, 0)
    camera.vertical_fov = 40
    camera.initialize_camera()
    scene = Scene(settings, two_perlin_spheres(), camera)

    return scene


if __name__ == "__main__":
    print("starting render...")
    start_time = time.time()
    scene = build_scene()
    scene.render()
    end_time = time.time()
    diff = end_time - start_time
    print("Done...\nTime: %s minutes" % (diff / 60.))
