class Intersection:

    def __init__(self):
        self.point = None
        self.normal = None
        self.distance = None
        self.front_face = False
        self.primitive = None
        self.material = None

    def set_face_normal(self, ray, outward_normal):
        self.front_face = ray.direction.dot(outward_normal) < 0.0
        self.normal = outward_normal if self.front_face else -outward_normal
