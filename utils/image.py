class Image:
    """Basic image to write raw ppm data """
    def __init__(self, width, aspect_ratio=16./9.):
        self.width = width
        self.height = int(width / aspect_ratio)
       
        self.aspect_ratio = aspect_ratio
        self.pixels = [[None for _ in range(self.height)] for _ in range(self.width)]
        
    def set_pixel(self, x, y, pixel_color):
        self.pixels[x][y] = pixel_color  # TODO: this may need to change in the next iteration
        
    def _write_header(self, image_fileobj):
        image_fileobj.write("P3 {} {}\n255\n".format(self.width, self.height))
        
    def _write_raw(self, img_fileobj):
        def to_byte(color_item):
            return round(max(min(color_item * 255,255), 0))
        
        for row in self.pixels:
            for color in row:
                img_fileobj.write("{} {} {} ".format(to_byte(color.red),to_byte(color.green),to_byte(color.blue)))
            
            img_fileobj.write("\n")
    
    def write_ppm_file(self, img_fileobj):
        self._write_header(img_fileobj)
        self._write_raw(img_fileobj)
