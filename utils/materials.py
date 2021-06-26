from abc import abstractmethod, ABC

from utils.colors import RGBColor


class Material(ABC):

    def __init__(self, name='base_material'):
        self.name = name

    @abstractmethod
    def scatter(self, ray_in, isect, color, ray_scattered):
        pass




class Checkered(Material):

    def __init__(self, even_color=RGBColor(1,1,1), odd_color=RGBColor(0,0,0)):
        super().__init__("checkered_material")
        self.even_color = even_color
        self.odd_color = odd_color


    def scatter(self, ray_in, isect, color, ray_scattered):
        pass