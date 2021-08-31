

class SceneSettings:

    def __init__(self, samples_per_pixel=10, max_depth=5, aspect_ratio=1.0, image_width=400):

        self.samplesperpixel = samples_per_pixel
        self.max_depth = max_depth
        self.image_file_name = "test_image.ppm"
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
