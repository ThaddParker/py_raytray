from utils.camera import Camera
from utils.colors import RGBColor
from utils.materials import Diffuse, DiffuseLight
from utils.scene import Scene
from utils.scene_settings import SceneSettings
from utils.shapes import Sphere, Rectangle, PrimitiveList
from utils.textures import Perlin, Pigment
from vectormath import Vector3


def simplelight():
    objects = PrimitiveList()
    perlintext = Perlin(4)
    objects.add(Sphere(Vector3(0, -1000, 0), 1000, Diffuse(perlintext)))
    objects.add(Sphere(Vector3(0, 2, 0), 2, Diffuse(perlintext)))

    difflight = DiffuseLight(RGBColor(4, 4, 4))
    objects.add(Rectangle((3, 5), (1, 3), -2, difflight))

    return objects


def build_scene():
    settings = SceneSettings(100, 5, 16 / 9, 400)
    settings.image_file_name = "simplelight.ppm"
    camera = Camera(Vector3(26, 3, 6), Vector3(0, 2, 0), settings.aspect_ratio)
    camera.vup = Vector3(0, 1, 0)
    camera.vertical_fov = 20.
    camera.initialize_camera()

    scene = Scene(settings, simplelight(), camera)
    scene.background = Pigment(RGBColor(0, 0, 0))
    return scene


if __name__ == "__main__":
    scene = build_scene()
    scene.render()
