"""Colormath doesn't work in multi-threading, so we need to create a simple rgb format"""

import numbers

from utils.functs import random_double


class RGBColor:
    """A [0..1] decimal value for high quality color"""

    def __init__(self, r=0., g=0., b=0., name='unnamed_color'):
        self.red = r
        self.green = g
        self.blue = b
        self.name = name

    def __str__(self) -> str:
        r = "{:.6f}".format(self.red)
        g = "{:.6f}".format(self.green)
        b = "{:.6f}".format(self.blue)
        return "(" + r + "," + g + "," + b + ")"

    def __repr__(self) -> str:
        r = "{:.6f}".format(self.red)
        g = "{:.6f}".format(self.green)
        b = "{:.6f}".format(self.blue)
        return "RGBColor(" + r + "," + g + "," + b + ")"

    def __iter__(self):
        return [self.red, self.green, self.blue].__iter__()

    @staticmethod
    def random(minval=0.0, maxval=1.0):
        red = random_double(minval, maxval)
        green = random_double(minval, maxval)
        blue = random_double(minval, maxval)
        return RGBColor(red, green, blue)

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
            raise ValueError(
                f"The key: {key} and value: {value} is invalid. Either use an integer or string for the key and use float value for the value field")

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
        return RGBColor(float(value) * self.red, float(value) * self.green, float(value) * self.blue)

    def __mul__(self, other):
        if isinstance(other, RGBColor):
            return RGBColor(other.red * self.red, other.green * self.green, other.blue * self.blue)
        else:
            return RGBColor(float(other) * self.red, float(other) * self.green, float(other) * self.blue)

    def __add__(self, value):
        if isinstance(value, RGBColor):
            return RGBColor(self.red + value.red, self.green + value.green, self.blue + value.blue)
        return RGBColor(self.red + value, self.green + value, self.blue + value)

    def __radd__(self, other):
        return RGBColor(self.red + other, self.green + other, self.blue + other)


# named colors
Black = RGBColor(0.0, 0.0, 0.0, "black")
White = RGBColor(1.0, 1.0, 1.0, "white")
Red = RGBColor(1.0, 0.0, 0.0, "red")
Green = RGBColor(0.0, 1.0, 0.0, "green")
Blue = RGBColor(0.0, 0.0, 1.0, "blue")

# These grays are useful for fine-tuning lighting color values
# and for other areas where subtle variations of grays are needed.
# PERCENTAGE GRAYS:
Gray05 = White * 0.05
Gray10 = White * 0.10
Gray15 = White * 0.15
Gray20 = White * 0.20
Gray25 = White * 0.25
Gray30 = White * 0.30
Gray35 = White * 0.35
Gray40 = White * 0.40
Gray45 = White * 0.45
Gray50 = White * 0.50
Gray55 = White * 0.55
Gray60 = White * 0.60
Gray65 = White * 0.65
Gray70 = White * 0.70
Gray75 = White * 0.75
Gray80 = White * 0.80
Gray85 = White * 0.85
Gray90 = White * 0.90
Gray95 = White * 0.95

# OTHER GRAYS
DimGray = RGBColor(0.329412, 0.329412, 0.329412, "dimgray")
DimGrey = RGBColor(0.329412, 0.329412, 0.329412, "dimgrey")
Gray = RGBColor(0.752941, 0.752941, 0.752941, "gray")
Grey = RGBColor(0.752941, 0.752941, 0.752941, "grey")
LightGray = RGBColor(0.658824, 0.658824, 0.658824, "lightgray")
LightGrey = RGBColor(0.658824, 0.658824, 0.658824, "lightgrey")
VLightGray = RGBColor(0.80, 0.80, 0.80, "verylightgray")
VLightGrey = RGBColor(0.80, 0.80, 0.80, "verylightgrey")

Aquamarine = RGBColor(0.439216, 0.858824, 0.576471, "aquamarine")
BlueViolet = RGBColor(0.62352, 0.372549, 0.623529, "blueviolet")
Brown = RGBColor(0.647059, 0.164706, 0.164706, "brown")
CadetBlue = RGBColor(0.372549, 0.623529, 0.623529, "cadetblue")
Coral = RGBColor(1.0, 0.498039, 0.0, "coral")
CornflowerBlue = RGBColor(0.258824, 0.258824, 0.435294, "cornflowerblue")
DarkGreen = RGBColor(0.184314, 0.309804, 0.184314,"darkgreen")
DarkOliveGreen = RGBColor(0.309804, 0.309804, 0.184314, "darkolivegreen")
DarkOrchid = RGBColor(0.6, 0.196078, 0.8, "darkorchid")
DarkSlateBlue = RGBColor(0.119608, 0.137255, 0.556863, "darkslateblue")
DarkSlateGray = RGBColor(0.184314, 0.309804, 0.309804, "darkslategray")
DarkSlateGrey = RGBColor(0.184314, 0.309804, 0.309804, "darkslategrey")
DarkTurquoise = RGBColor(0.439216, 0.576471, 0.858824, "darkturquoise")
Firebrick = RGBColor(0.556863, 0.137255, 0.137255, "firebrick")
ForestGreen = RGBColor(0.137255, 0.556863, 0.137255, "forestgreen")
Gold = RGBColor(0.8, 0.498039, 0.196078, "gold")
Goldenrod = RGBColor(0.858824, 0.858824, 0.439216, "goldenrod")
GreenYellow = RGBColor(0.576471, 0.858824, 0.439216, "greenyellow")
IndianRed = RGBColor(0.309804, 0.184314, 0.184314, "indianred")
Khaki = RGBColor(0.623529, 0.623529, 0.372549, "khaki")
LightBlue = RGBColor(0.74902, 0.847059, 0.847059, "lightblue")
LightSteelBlue = RGBColor(0.560784, 0.560784, 0.737255, "lightsteelblue")
LimeGreen = RGBColor(0.196078, 0.8, 0.196078, "limegreen")
Maroon = RGBColor(0.556863, 0.137255, 0.419608, "maroon")
MediumAquamarine = RGBColor(0.196078, 0.8, 0.6, "mediumaquamarine")
MediumBlue = RGBColor(0.196078, 0.196078, 0.8, "mediumblue")
MediumForestGreen = RGBColor(0.419608, 0.556863, 0.137255, "mediumforestgreen")
MediumGoldenrod = RGBColor(0.917647, 0.917647, 0.678431, "mediumgoldenrod")
MediumOrchid = RGBColor(0.576471, 0.439216, 0.858824, "mediumorchid")
MediumSeaGreen = RGBColor(0.258824, 0.435294, 0.258824, "mediumseagreen")
MediumSlateBlue = RGBColor(0, 0.498039, 1.0) # TODO: Fixme here if this is correct color
MediumSpringGreen = RGBColor(0, 0.498039, 1.0) # TODO: see above
MediumTurquoise = RGBColor(0.439216, 0.858824, 0.858824, "mediumturquoise")
MediumVioletRed = RGBColor(0.858824, 0.439216, 0.576471, "mediumvioletred")
MidnightBlue = RGBColor(0.184314, 0.184314, 0.309804, "midnightblue")
Navy = RGBColor(0.137255, 0.137255, 0.556863, "navy")
NavyBlue = RGBColor(0.137255, 0.137255, 0.556863, "navyblue")
Orange = RGBColor(1, 0.5, 0.0, "orange")
OrangeRed = RGBColor(1.0, 0.25, 0.0, "orangered")
Orchid = RGBColor(0.858824, 0.439216, 0.858824, "orchid")
PaleGreen = RGBColor(0.560784, 0.737255, 0.560784, "palegreen")
Pink = RGBColor(0.737255, 0.560784, 0.560784, "pink")
Plum = RGBColor(0.917647, 0.678431, 0.917647, "plum")
Salmon = RGBColor(0.435294, 0.258824, 0.258824, "salmon")
SeaGreen = RGBColor(0.137255, 0.556863, 0.419608, "seagreen")
Sienna = RGBColor(0.556863, 0.419608, 0.137255, "sienna")
SkyBlue = RGBColor(0.196078, 0.6, 0.8, "skyblue")
SlateBlue = RGBColor(0.0, 0.498039, 1.0, "slateblue")
SpringGreen = RGBColor(0.0, 1.0, 0.498039, "springgreen")
SteelBlue = RGBColor(0.137255, 0.419608, 0.556863, "steelblue")
Tan = RGBColor(0.858824, 0.576471, 0.439216, "tan")
Thistle = RGBColor(0.847059, 0.74902, 0.847059, "thistle")
Turquoise = RGBColor(0.678431, 0.917647, 0.917647, "turquoise")
Violet = RGBColor(0.309804, 0.184314, 0.309804, "violet")
VioletRed = RGBColor(0.8, 0.196078, 0.6, "violetred")
Wheat = RGBColor(0.847059, 0.847059, 0.74902, "wheat")
YellowGreen = RGBColor(0.6, 0.8, 0.196078, "yellowgreen")
SummerSky = RGBColor(0.22, 0.69, 0.87, "summersky")
RichBlue = RGBColor(0.35, 0.35, 0.67, "richblue")
Brass = RGBColor(0.71, 0.65, 0.26, "brass")
Copper = RGBColor(0.72, 0.45, 0.20, "copper")
Bronze = RGBColor(0.55, 0.47, 0.14, "bronze")
Bronze2 = RGBColor(0.65, 0.49, 0.24, "bronze2")
Silver = RGBColor(0.90, 0.91, 0.98, "silver")
BrightGold = RGBColor(0.85, 0.85, 0.10, "brightgold")
OldGold = RGBColor(0.81, 0.71, 0.23, "oldgold")
Feldspar = RGBColor(0.82, 0.57, 0.46, "feldspar")
Quartz = RGBColor(0.85, 0.85, 0.95, "quartz")
Mica = Black  # needed in textures.inc
NeonPink = RGBColor(1.00, 0.43, 0.78, "neonpink")
DarkPurple = RGBColor(0.53, 0.12, 0.47, "darkpurple")
NeonBlue = RGBColor(0.30, 0.30, 1.00, "neonblue")
CoolCopper = RGBColor(0.85, 0.53, 0.10, "coolcopper")
MandarinOrange = RGBColor(0.89, 0.47, 0.20, "mandarinorange")
LightWood = RGBColor(0.91, 0.76, 0.65, "lightwood")
MediumWood = RGBColor(0.65, 0.50, 0.39, "mediumwood")
DarkWood = RGBColor(0.52, 0.37, 0.26, "darkwood")
SpicyPink = RGBColor(1.00, 0.11, 0.68, "spicypink")
SemiSweetChoc = RGBColor(0.42, 0.26, 0.15, "semisweetchocolate")
BakersChoc = RGBColor(0.36, 0.20, 0.09, "bakerschocolate")
Flesh = RGBColor(0.96, 0.80, 0.69, "flesh")
NewTan = RGBColor(0.92, 0.78, 0.62, "newtan")
NewMidnightBlue = RGBColor(0.00, 0.00, 0.61, "newmidnightblue")
VeryDarkBrown = RGBColor(0.35, 0.16, 0.14, "verydarkbrown")
DarkBrown = RGBColor(0.36, 0.25, 0.20, "darkbrown")
DarkTan = RGBColor(0.59, 0.41, 0.31, "darktan")
GreenCopper = RGBColor(0.32, 0.49, 0.46, "greencopper")
DkGreenCopper = RGBColor(0.29, 0.46, 0.43, "darkgreencopper")
DustyRose = RGBColor(0.52, 0.39, 0.39, "dustyrose")
HuntersGreen = RGBColor(0.13, 0.37, 0.31, "huntersgreen")
Scarlet = RGBColor(0.55, 0.09, 0.09, "scarlet")

Med_Purple = RGBColor(0.73, 0.16, 0.96, "mediumpurple")
Light_Purple = RGBColor(0.87, 0.58, 0.98, "lightpurple")
Very_Light_Purple = RGBColor(0.94, 0.81, 0.99, "verylightpurple")
