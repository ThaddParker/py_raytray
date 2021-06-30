import math

from vectormath import Vector3

from utils.functs import degrees_to_radians, random_in_unit_disk
from utils.ray import Ray


class Camera:
    
    def __init__(self,origin, look_at, aspect_ratio=1.0) -> None:
        self.vertical_fov = 40.0
        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0

        self.origin = origin
        self.look_at = look_at
        self.vup = Vector3(0,1,0)
        self.horizontal = Vector3(self.viewport_width, 0, 0)
        self.vertical = Vector3(0, self.viewport_height, 0)
        self.lower_left = self.origin - self.horizontal / 2.0 - self.vertical / 2.0 - Vector3(0, 0, self.focal_length)
        self.aperture = 2.0
        self.lens_radius = self.aperture /2.0
        self.w = None
        self.u = None
        self.v = None
        self.focus_distance = 10.

    def initialize_camera(self):
        theta = degrees_to_radians(self.vertical_fov)
        hght = math.tan(theta/2.)
        self.viewport_height = 2.0 * hght
        self.viewport_width = self.aspect_ratio * self.viewport_height

        self.w = (self.origin - self.look_at).normalize()
        self.u = (self.vup.cross(self.w)).normalize()
        self.v = self.w.cross(self.u)


        self.horizontal = self.focus_distance* self.viewport_width * self.u
        self.vertical = self.focus_distance* self.viewport_height * self.v

        self.lower_left = self.origin - self.horizontal / 2.0 - self.vertical / 2.0 - self.focus_distance*self.w
        self.lens_radius = self.aperture / 2.

    def create_ray(self, x, y):
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y
        ray_dir = self.lower_left + x*self.horizontal + y*self.vertical - self.origin - offset
        return Ray(self.origin + offset, ray_dir)
