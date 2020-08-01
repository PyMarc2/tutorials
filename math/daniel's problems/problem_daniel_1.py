'''
__AUTHOR__  :   Marc-André Vigneault
__CREDITS__ :   Olivier Dorion-Theriault, Franccoise Meunier,
__DATE__    :   21/07/2020, 20:28
'''


import numpy as np
import matplotlib.pyplot as plt
import random
import time

number_of_people = 25000
x = np.linspace(1, number_of_people, number_of_people)
nbOfTries = 1000
fig, ax = plt.subplots(1, 2)
counterTries = 0
smallSample = 40

statisticList = [0]*nbOfTries

for j in range(0, nbOfTries):
    list_of_number = list(np.linspace(1, number_of_people, number_of_people))
    number_of_people_that_left = 0
    picked_numbers = [0]*smallSample
    estimation_of_people = [0]*smallSample
    normalized_estimation = [0]*smallSample
    #print("time1")
    for i in range(0, smallSample):
        number_of_people_that_left += 1
        # print("append {}".format(time.time_ns()))
        picked_numbers[i] = (random.choice(list_of_number))
        # print("random choice {}".format(time.time_ns()))
        list_of_number.remove(picked_numbers[i])
        # print("append {}".format(time.time_ns()))
        estimation_of_people[i] = (max(picked_numbers) + (max(picked_numbers)+number_of_people_that_left)/number_of_people_that_left)
        normalized_estimation[i] = round(estimation_of_people[i]/number_of_people, 3)
        # print("estimation maximale {}".format(time.time_ns()))
    statisticList[j] = estimation_of_people
    counterTries += 1
    print("Progrès: {}%".format(counterTries*100/nbOfTries))
    ax[0].plot(x[0:smallSample], normalized_estimation)
    ax[0].set_ylabel("$\delta$ (N) Normalized Estimator's value")
    ax[0].set_xlabel("Sample size (a. u.)")

statisticList = np.array(statisticList)
print("time3")
for i in range(10, smallSample, 5):
    column = np.round(np.array(statisticList[:, i])/number_of_people, 3)
    ax[1].hist(column, 80, label="{}".format(i))
    ax[1].legend()
    ax[1].set_xlabel("$\delta$(N) Normalized Estimator's value")
    ax[1].set_ylabel("count")
    ax[1].set_xlim(0.85, 1.15)

plt.tight_layout()
plt.savefig("daniels_solution.pdf", dpi=600)

