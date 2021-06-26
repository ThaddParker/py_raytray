from vectormath import Vector3
from utils.ray import Ray


class Camera:
    
    def __init__(self) -> None:
        self.aspect_ratio = 16. / 9.
        self.viewport_height = 2.0
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0

        self.origin = Vector3(0, 0, 0)
        self.horizontal = Vector3(self.viewport_width, 0, 0)
        self.vertical = Vector3(0, self.viewport_height, 0)
        self.lower_left = self.origin - self.horizontal / 2.0 - self.vertical / 2.0 - Vector3(0, 0, self.focal_length)

    def create_ray(self, x, y):
        ray_dir = self.lower_left + x*self.horizontal + y*self.vertical - self.origin
        return Ray(self.origin, ray_dir)
