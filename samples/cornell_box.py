from utils.camera import Camera
from utils.colors import RGBColor
from utils.materials import Diffuse, DiffuseLight
from utils.scene import Scene
from utils.scene_settings import SceneSettings
from utils.shapes import PrimitiveList, Rectangle
from utils.textures import Pigment
from vectormath import Vector3


def cornell_box():
    red = Diffuse(Pigment(RGBColor(.65, 0.05, 0.05)))
    white = Diffuse(Pigment(RGBColor(.73, .73, 0.73)))
    green = Diffuse(Pigment(RGBColor(0.12, 0.45, 0.15)))
    light = DiffuseLight(RGBColor(15, 15, 15))

    objects = PrimitiveList()
    objects.add(Rectangle((0, 555), (0, 555), 555, green, 'yz'))
    objects.add(Rectangle((0, 555), (0, 555), 555, red, 'yz'))
    objects.add(Rectangle((213, 343), (227, 332), 555, light, 'xz'))
    objects.add(Rectangle((0, 555), (0, 555), 0, white, 'xz'))
    objects.add(Rectangle((0, 555), (0, 555), 555, white, 'xz'))
    objects.add(Rectangle((0, 555), (0, 555), 555, white, 'xy'))

    return objects


def build_scene():
    world = cornell_box()
    aspect_ratio = 1.0
    image_width = 600
    samples_per_pixel = 200
    background = Pigment(RGBColor(0, 0, 0))
    origin = Vector3(278, 278, -800)
    lookat = Vector3(278, 278, 0)
    vfov = 40
    camera = Camera(origin, lookat, aspect_ratio)
    camera.vertical_fov = vfov
    camera.initialize_camera()
    settings = SceneSettings(samples_per_pixel, 5, aspect_ratio, image_width)

    settings.image_file_name = "cornell_emptybox.ppm"
    scene = Scene(settings, world, camera)
    scene.background = background

    return scene


if __name__ == "__main__":
    scene = build_scene()
    scene.render()
