
import numpy as np
import matplotlib.pyplot as plt


class GeneralMovableObject:
    variableGenerale = 0

    def __init__(self):
        print('General Object Created.')
        self.x = 0
        self.y = 0

    def move(self, x, y):
        self.x += x
        self.y += y
        self.z = 2


class Robot(GeneralMovableObject):
    def __init__(self):
        super(Robot, self).__init__()


objet1 = Robot()


figure = plt.figure()
ax = figure.add_subplot(111)

x = np.linspace(0, 10, 100)
y = np.cos(x)

ax.plot(x, y)
figure.show()