from manimlib.imports import *
from manimlib import *
import math


class Graphing(Scene):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "y_min": -4,
        "y_max": 4,
        "graph_origin": ORIGIN,
        "function_color": WHITE,
        "axes_color": BLUE
    }

    def construct(self):

        self.play(DrawBorderThenFill(TexMobject("bonjour")))
        self.wait(1)

    @staticmethod
    def func_x2(x):
        return x**2

    @staticmethod
    def func_x3(x):
        return x**3

    @staticmethod
    def func_gaussian(x, mu=0, s=1):
        return (4/(s*math.sqrt(2*math.pi)))*math.exp(-(x-mu)**2/(2*s**2))



[
    [[],[],[],[],[],],
    [],
    [],
]