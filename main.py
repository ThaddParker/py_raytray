from utils.boundingvolume import BoundingVolumeNode
from utils.camera import Camera
from utils.functs import random_double, random_in_unit_sphere, random_unit_vector, random_in_hemisphere
from utils.image import Image
from utils.colors import RGBColor
from utils.interval import Interval
from utils.materials import Diffuse, Metal, Refractive
from utils.primitive_list import PrimitiveList
from utils.scene import Scene
from utils.scene_settings import SceneSettings
from utils.shapes import Sphere
from utils.textures import Checker, Pigment, Perlin
import time
from tqdm import tqdm
from vectormath import Vector3
import math

def main():
    print("ok")
    settings = SceneSettings(1000, 50, (16. / 9.), image_width=800)
    # settings.image_width = 1200

    # samplesperpixel = 100
    # maxdepth = 50
    # image = Image(400)
    camera = Camera(Vector3(1, 2, 2), Vector3(0, 0, 0), settings.aspect_ratio)
    camera.vup = Vector3(0, 1, 0)
    camera.vertical_fov = 45
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
    matperlin = Diffuse(Perlin(4))
    matchecker = Diffuse(Checker(0.25, RGBColor(0, 0, 0), RGBColor(1, 1, 1)))
    matrefractive = Refractive(RGBColor(1,1,1),1.5)

    sceneobjs.add(Sphere(Vector3(0, 1, -1), 1, matleft))
    sceneobjs.add(Sphere(Vector3(1, 0, -1), 1, matrefractive))
    sceneobjs.add(Sphere(Vector3(0, -1000.5, -1), 1000, matground))
    sceneobjs.add(Sphere(Vector3(-3, 1, -1), 0.5, matleft))
    sceneobjs.add(Sphere(Vector3(1,3, -1), 0.5, matright))
    # aa = BoundingVolumeNode(sceneobjs)
    # bb = PrimitiveList(aa)
    scene = Scene(settings, sceneobjs, camera)

    scene.render()
    t1 = time.time()
    diff = t1 - t0
    print("Done...\nTime: %s minutes" % (diff / 60.))


if __name__ == "__main__":
    main()
