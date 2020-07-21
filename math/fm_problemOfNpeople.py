import numpy as np
import matplotlib.pyplot as plt
import random

number_of_people = 5000
x = np.linspace(1, number_of_people, number_of_people)
nbOfTries = 500
fig, ax = plt.subplots(1, 2)

statisticList = []

for j in range(0, nbOfTries):
    list_of_number = list(np.linspace(1, number_of_people, number_of_people))
    number_of_people_that_left = 0
    picked_numbers = []
    estimation_of_people = []

    for i in range(len(list_of_number)):
        number_of_people_that_left += 1
        picked_numbers.append(random.choice(list_of_number))
        list_of_number.remove(picked_numbers[-1])
        estimation_of_people.append(2*sum(picked_numbers)/number_of_people_that_left)

    statisticList.append(estimation_of_people)

    ax[0].plot(x, estimation_of_people)

statisticList = np.array(statisticList)

for i in range(50, 800, 100):
    column = np.array(statisticList[:, i])
    print(column)
    ax[1].hist(column, label="{}".format(i))
    ax[1].legend()

plt.show()
