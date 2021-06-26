
"""Colormath doesn't work in multi-threading, so we need to create a simple rgb format"""

import numbers

class RGBColor:
    """A [0..1] decimal value for high quality color"""
    
    def __init__(self, r=0.,g=0.,b=0.,name='unnamed_color'):
        self.red = r
        self.green = g
        self.blue = b
        self.name = name
        
    def __str__(self) -> str:
        r = "{:.6f}".format(self.red)
        g = "{:.6f}".format(self.green)
        b = "{:.6f}".format(self.blue)
        return "("+r+","+g+","+b +")"
        
    def __repr__(self) -> str:
        r = "{:.6f}".format(self.red)
        g = "{:.6f}".format(self.green)
        b = "{:.6f}".format(self.blue)
        return "RGBColor("+r+","+g+","+b +")"
        
    def __iter__(self):
        return [self.red,self.green,self.blue].__iter__()
        
    def __setitem__(self, key, value):
        if isinstance(key, int) and (isinstance(value, int) or isinstance(value, numbers.Number)):
            if key == 0:
                self.red = value
            elif key == 1:
                self.green = value
            elif key == 2:
                self.blue = value
        elif isinstance(key, str):
            if str(key).lower() == 'red' or str(key).lower() == 'r':
                self.red = value
            elif str(key).lower() == 'green' or str(key).lower() == 'g':
                self.green = value
            elif str(key).lower() == 'blue' or str(key).lower() == 'b':
                self.blue = value
        else:
            raise ValueError(f"The key: {key} and value: {value} is invalid. Either use an integer or string for the key and use float value for the value field")

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.red
            elif item == 1:
                return self.green
            elif item == 2:
                return self.blue
            else:
                raise IndexError(f"The provided index: {item} is invalid. Please provide [0, 1, 2] only")
        elif isinstance(item, str):
            if str(item).lower() == 'red' or str(item).lower() == 'r':
                return self.red
            elif str(item).lower() == 'green' or str(item).lower() == 'g':
                return self.green
            elif str(item).lower() == 'blue' or str(item).lower() == 'b':
                return self.blue
            raise IndexError(f"The provided index name: {item} is invalid. Please provide either 'red','green','blue'")
        
    def __rmul__(self, value):
        return RGBColor(value * self.red,value*self.green,value*self.blue)
    
    def __add__(self, value):
        if isinstance(value, RGBColor):
            return RGBColor(self.red + value.red, self.green + value.green,self.blue+value.blue)
        return RGBColor(self.red + value, self.green + value, self.blue+value)

    def __radd__(self, other):
        return RGBColor(self.red + other, self.green + other, self.blue + other)