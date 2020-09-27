import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os
import optimiser
from mpl_toolkits.mplot3d import Axes3D
import json

def plot(title, opt, directory):
    if not directory[-1] in ('/', '\\'):
        directory+='/'
    time_now = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    dir_name = directory + "logs/" + time_now
    create_dir(dir_name)
    create_objectives_log(opt, dir_name)
    create_sol_log(opt, dir_name, title)
    graph(dir_name + "/objectives_log.txt", title)
    plt.savefig(dir_name + "/pareto_front.png")
    plt.show()

def graph(file, title=None):
    """Graph function is used for adding all the plots and the title to the 
    graph."""
    front = np.loadtxt(file)

    if len(front) == 2:
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

    elif ValueError:
        print("Incorrect number of dims in solution to graph.")

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
        print("Directory ", dir_name, " already exists")


def create_objectives_log(self, dir_name):
    """Creates objective log as a txt file by seperating each objective of a 
    solution by a space and each soluition by a new line."""
    front = self.hypercubes.output_front()
    try:
        output = open(dir_name + "/objectives_log.txt", "w+")

        for i in front:
            if len(i) == 4:
                print("{} {} {} {}".format(i[0], i[1], i[2], i[3]), file=output)
            elif len(i) == 3:
                print("{} {} {}".format(i[0], i[1], i[2]), file=output)
            elif len(i) == 2:
                print("{} {}".format(i[0], i[1]), file=output)
    except FileExistsError:
        print("File ", "objectives_log", " already exists")


def create_sol_log(self, dir_name, title):
    """Creates a solution log by creating a json file with an array of solution 
    objects from the pareto front."""
    big_cube = self.hypercubes.cube_dict
    data = {}
    data['title'] = title
    data['solutions'] = []
    try:
        for cube in big_cube:
            for sol in big_cube[cube]:
                data['solutions'].append(
                    {
                        'position': sol.x.tolist(),
                        'objectives': sol.objectives.tolist()
                    }
                )
        with open(dir_name + "/solutions_log.json", "w+") as outfile:
            json.dump(data, outfile, indent=4)
        
    except FileExistsError:
        print("File ", "solutions_log", " already exists")


if __name__ == "__main__":
    pass