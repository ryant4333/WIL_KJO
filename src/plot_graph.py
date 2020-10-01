import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os
import optimiser
from mpl_toolkits.mplot3d import Axes3D
import json


def plot(title, opt, directory):
    if not directory[-1] in ('/', '\\'):
        directory += '/'
    time_now = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    dir_name = directory + "logs/" + time_now
    create_dir(dir_name)
    create_objectives_log(opt.hypercubes.output_front(), dir_name)
    create_sol_log(opt.hypercubes.cube_dict, dir_name, title)
    graph(dir_name + "/objectives_log.txt", title)
    plt.savefig(dir_name + "/pareto_front.png")
    plt.show()


def graph(file, title=None):
    """Graph function is used for adding all the plots and the title to the 
    graph."""
    front = np.loadtxt(file)
    if len(front) == 0:
        raise ValueError("File is empty")
    elif len(front) == 2:
        plt.scatter(front[0], front[1], c='b')
    elif len(front) == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.scatter(front[0], front[1], front[2], c='b')
    elif len(front) == 4:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        img = ax.scatter(front[0], front[1], front[2], c=front[3], cmap=plt.cool())
        fig.colorbar(img)
    elif len(front) == 5:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        img = ax.scatter(front[0], front[1], front[2], c=front[3], s=front[4], cmap=plt.cool())
        fig.colorbar(img)

    elif len(front[0]) == 5:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        img = ax.scatter(front[:, 0], front[:, 1], front[:, 2], c=front[:, 3], s=front[:, 4] * 10, cmap=plt.cool())
        fig.colorbar(img)
    elif len(front[0]) == 4:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        img = ax.scatter(front[:, 0], front[:, 1], front[:, 2], c=front[:, 3], cmap=plt.cool())
        fig.colorbar(img)
    elif len(front[0]) == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(front[:, 0], front[:, 1], front[:, 2], c='b')
    elif len(front[0]) == 2:
        plt.scatter(front[:, 0], front[:, 1], c='b')

    else:
        raise ValueError("Incorrect number of dims in solution to graph.")

    if title != None:
        plt.title(title)
    plt.xlabel(r'$f_1(x)$')
    plt.ylabel(r'$f_2(x)$')
    plt.legend(["Front"])


def create_dir(dir_name):
    """Creates the directory where the graph, solutions log and the objective
    log is kept"""
    try:
        os.makedirs(dir_name)
        print("DIRECTORY CREATED: ", dir_name)
    except FileExistsError:
        raise FileExistsError("Directory ", dir_name, " already exists")


def create_objectives_log(self, dir_name):
    """Creates objective log as a txt file by seperating each objective of a
    solution by a space and each soluition by a new line."""
    front = self

    if not os.path.exists(dir_name + "/objectives_log.txt"):
        output = open(dir_name + "/objectives_log.txt", "w+")
    else:
        raise FileExistsError("File ", "objectives_log", " already exists")

    for i in front:
        if len(i) == 5:
            print("{} {} {} {} {}".format(i[0], i[1], i[2], i[3], i[4]), file=output)
        if len(i) == 4:
            print("{} {} {} {}".format(i[0], i[1], i[2], i[3]), file=output)
        elif len(i) == 3:
            print("{} {} {}".format(i[0], i[1], i[2]), file=output)
        elif len(i) == 2:
            print("{} {}".format(i[0], i[1]), file=output)
        else:
            raise ValueError("Invalid number of dimensions")


def create_sol_log(dict_, dir_name, title):
    """Creates a solution log by creating a json file with an array of solution
    objects from the pareto front."""
    big_cube = dict_
    data = {}
    data['title'] = title
    data['solutions'] = []

    for cube in big_cube:
        for sol in big_cube[cube]:
            data['solutions'].append(
                {
                    'position': sol.x.tolist(),
                    'objectives': sol.objectives.tolist()
                }
            )
    if not os.path.exists(dir_name + "/solutions_log.json"):
        with open(dir_name + "/solutions_log.json", "w+") as outfile:
            json.dump(data, outfile, indent=4)
    else:
        raise FileExistsError("File ", "solutions_log", " already exists")


if __name__ == "__main__":
    pass