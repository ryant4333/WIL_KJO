import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os
import optimiser
from mpl_toolkits.mplot3d import Axes3D as ax


def plot(title, opt, directory):
    if not directory[-1] in ('/', '\\'):
        directory+='/'
    time_now = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    dir_name = directory + "logs/" + time_now

    create_dir(dir_name)
    create_fitness_log(opt, dir_name)
    create_pos_log(opt, dir_name)

    front = np.loadtxt(dir_name + "/front_log")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if len(front) > 2:
        ax.scatter(front[:, 0], front[:, 1], front[:, 2], c='b', marker='o')
    else:
        plt.scatter(front[0], front[1], c='b')
    plt.title(title)
    plt.xlabel(r'$f_1(x)$')
    plt.ylabel(r'$f_2(x)$')
    ax.legend(["Front"])
    plt.savefig(dir_name + "/front.png")
    plt.show()


def create_dir(dir_name):
    try:
        os.makedirs(dir_name)
        print("DIRECTORY CREATED: ", dir_name)
    except FileExistsError:
        print("Directory ", dir_name, " already exists")


def create_fitness_log(self, dir_name):
    front = self.hypercubes.output_front()
    try:
        output = open(dir_name + "/front_log", "w+")
        for i in front:
            print("{} {} {}".format(i[0], i[1], i[2]), file=output)
    except FileExistsError:
        print("File ", "front_log", " already exists")


def create_pos_log(self, dir_name):
    big_cube = self.hypercubes.cube_dict
    count = 00000
    try:
        output = open(dir_name + "/N_D_Solutions", "w+")
        for cube in big_cube:
            for sol in big_cube[cube]:
                print("Solution ID: ", count, file=output)
                print("Fitness:{}".format(sol.objectives), file=output)
                print("Position:{}".format(sol.x), file=output)
                print("--------------------------------------------------------------------------------------", file=output)
                count += 1
    except FileExistsError:
        print("File ", "N_D_Solutions", " already exists")


if __name__ == "__main__":
    optimiser = optimiser.Optimiser("config.json")
    optimiser.run()

    plot(r'ZDT1 Search Domain: $0\leq x_i\leq1,1\leq i\leq30.\mathrm{}$', optimiser)
    plt.show()


