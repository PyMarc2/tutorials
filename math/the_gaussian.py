'''
If we have a dice, that we throw twice, the sum of the two numbers can vary from [2, 12].

What is the probability of getting any number on a given throw. p=(1/6) right? Because all 6 numbers have the same possibility of getting picked.

The possibility of getting some two numbers, let's say [1,3] would be the probability of one * the second one right? Because these are two separate events.

So the probability of getting [1,3] is = (1/6)*(1/6), as is any other combination fo 2 numbers.

Thus, what is the possibility of getting the sum of 5? Is it simply (1/6)*(1/6) = 1/36 because the 2 even were independent?

No. What can give 5? [[1+4], [4+1], [3+2], [2+3]]. Each of these 4 combinations have the possibility 1/36, so the total probability of getting 5 is the sum
Of the probabilities, so (4/36=1/9)

So for a random variable X, that can take any number from [1, N], with a uniform probability mass, say every number has
the probability (1/N) of getting picked

So, for the sum of two random variables X + Y, it will lead to a third random variable Z.
The goal is to find the probability density of the Z variable.

What does the variable Y needs to be to give in order for the Z to give z. In other terms: X=x, Z=z, so Y=z-x

Thus, the probability of Z=z is:  P(Z=z) = sum( P(X=x) * P(Y=z-x) )

This is the very definition of the convolution: f*g (z) = sum ( f(x) * g(z-x) )

'''
import numpy as np
from numpy import convolve
from matplotlib import pyplot as plt
import random


# class GaussianTutorial:
#     def __init__(self, N):
#         self.N = N
#         self.X1 = [1/N for i in range(1, N)]
#         self.X2 = [1/N for j in range(1, N)]
#         self.X3 = []
#         self.fig, self.ax = plt.subplots()
#
#     def convolute_square(self):
#         self.X3 = convolve(self.X1, self.X2)
#         self.X1 = self.X3
#         return self.X3
#
#     def launch_sequence(self, n):
#         for i in range(1, n):
#             Y = self.convolute_square()
#             X = np.linspace(1, len(Y), len(Y))
#             self.ax.plot(X, Y)
#         plt.show()
#
# gt = GaussianTutorial(20)
# gt.launch_sequence(3)

number_of_people_in_the_room = 900
number_of_people_that_left = 0
list_of_number = list(np.linspace(1, number_of_people_in_the_room, number_of_people_in_the_room))
picked_number = []
number_over_people = []


for i in range(len(list_of_number)):
    picked_number.append(random.choice(list_of_number))
    list_of_number.remove(picked_number[-1])
    number_of_people_that_left += 1
    number_over_people.append(sum(picked_number)/number_of_people_that_left)

print(number_of_people_that_left)

plt.plot(np.linspace(0, number_of_people_that_left, number_of_people_in_the_room)[0:200], number_over_people[0:200])

plt.show()

<<<<<<< Updated upstream

class GaussianTutorial:
    def __init__(self, N):
        self.N = N
        self.amountPicked = 0
        self.X1 = [1/N for _ in range(1, N)]
        self.X2 = [1/N for _ in range(1, N)]
        self.X3 = []
        self.fig, self.ax = plt.subplots()

    def convolve_last_two(self):
        self.X3 = convolve(self.X1, self.X2)
        self.X1 = self.X3
        return self.X3

    def launch_sequence(self, n):
        for i in range(0, n):
            self.amountPicked += 1
            self.X2 = [1/(self.N-self.amountPicked) for _ in range(1, self.N-self.amountPicked)]
            if i == 0:
                X = np.linspace(1, len(self.X1), len(self.X1))
                self.ax.plot(X, self.X1)
            else:
                Y = self.convolve_last_two()
                X = np.linspace(1, len(Y), len(Y))
                self.ax.plot(X, Y)  
                print((len(Y)/2)/self.amountPicked)
        plt.show()



gt = GaussianTutorial(20)
gt.launch_sequence(18)

=======
>>>>>>> Stashed changes
