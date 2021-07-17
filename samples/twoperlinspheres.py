from utils.camera import Camera
from utils.materials import Diffuse
from utils.scene import Scene
from utils.scene_settings import SceneSettings
from utils.shapes import Sphere, PrimitiveList
from utils.textures import Perlin
from vectormath import Vector3

def two_perlin_spheres():

    objects = PrimitiveList()

    perlin_texture = Perlin(4)

    objects.add(Sphere(Vector3(0,-1000, 0),1000,Diffuse(perlin_texture)))
    objects.add(Sphere(Vector3(0, 2, 0), 2, Diffuse(perlin_texture)))

    return objects

def build_scene():
    settings = SceneSettings(100,5, 16/9,400)
    camera = Camera(Vector3(13,2,3),Vector3(0,0,0), settings.aspect_ratio)
    settings.image_file_name = "twoperlinspheres.ppm"
    camera.aperture = 0.
    camera.vup = Vector3(0,1,0)
    camera.vertical_fov = 20
    camera.initialize_camera()
    scene = Scene(settings, two_perlin_spheres(),camera)

    return scene


if __name__ == "__main__":
    scene = build_scene()
    scene.render()
