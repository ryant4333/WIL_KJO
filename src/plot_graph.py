import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os
from optimiser import *
from mpl_toolkits.mplot3d import Axes3D
import json
"""
 plot_graph.py is used for logging and plotting the non dominated solutions found by the optimiser.
 When the optimiser reaches a stopping condition and stops running, it calls on the plotter to create a timestamped
 in the the chosen path. Each timestamped directory contains 3 files.
 
 objectives_log.txt:    A collection of non-dominated solutions. This file is mainly for plotting purposes.
 pareto_front.png:      All solutions in the objectives_log.txt graphed into matplotlib.
 solutions_log.json:    A full json log of found non-dominated solutions with relative fitness and positions.
   
"""

def plot(title: str, opt, directory: str) -> None:
    if not directory[-1] in ('/', '\\'):
        directory += '/'
    time_now = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    dir_name = directory + "logs/" + time_now
    create_dir(dir_name)
    create_sol_log(opt.hypercubes.cube_dict, dir_name, title)
    create_objectives_log(opt.hypercubes.output_front(), dir_name)
    graph(dir_name + "/objectives_log.txt", title)
    plt.savefig(dir_name + "/pareto_front.png")
    plt.show()


def graph(file: str, title: str = None) -> None:
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


def create_dir(dir_name: str) -> None:
    """Creates the directory where the graph, solutions log and the objective
    log is kept"""
    try:
        os.makedirs(dir_name)
        print("DIRECTORY CREATED: ", dir_name)
    except FileExistsError:
        raise FileExistsError("Directory ", dir_name, " already exists")


def create_objectives_log(front: list, dir_name: str) -> None:
    """Creates objective log as a txt file by seperating each objective of a
    solution by a space and each soluition by a new line."""

    if not os.path.exists(dir_name + "/objectives_log.txt"):
        output = open(dir_name + "/objectives_log.txt", "w+")
    else:
        raise FileExistsError("File ", "objectives_log", " already exists")

    for i in front:
        s = " ".join(map(str, i))
        print(s, file=output)


def create_sol_log(big_cube: dict, dir_name: str, title: str) -> None:
    """Creates a solution log by creating a json file with an array of solution
    objects from the pareto front."""
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