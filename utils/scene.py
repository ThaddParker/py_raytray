from utils.colors import RGBColor
from utils.functs import random_double
from utils.image import Image
from tqdm import tqdm

class Scene:
    def __init__(self,scene_settings, camera):
        self.scene_settings = scene_settings
        self.image = Image(scene_settings.image_width)
        self.camera = camera

    def render(self):
        with open("first_test.ppm", "w") as img_file:
            img_file.write("P3 {} {}\n255\n".format(self.image.width, self.image.height))
            for j in tqdm(reversed(range(self.image.height))):
                for i in range(self.image.width):
                    pixel_color = RGBColor(0, 0, 0)
                    for s in range(samplesperpixel):
                        x = float(i + random_double()) / self.image.width
                        y = float(j + random_double()) / self.image.height
                        ray = self.camera.create_ray(x, y)
                        pixel_color += ray_color(ray, scene,
                                                 maxdepth)  # RGBColor(float(i)/image.width, float(j)/image.height, 0.25)
                        # image.set_pixel(i, j, pixel_color)

                    write_color(img_file, pixel_color, samplesperpixel)
                    # img_file.write(
                    #     "{} {} {} ".format(to_byte(pixel_color.red), to_byte(pixel_color.green), to_byte(pixel_color.blue)))
                img_file.write("\n")