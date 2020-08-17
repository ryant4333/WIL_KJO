import json
import numpy as np
import zdt_test as zdt


class Problem:
    """
    Problem config class
    """
    def __init__(self, config_file):
        # Read data from JSON file
        with open(config_file) as f:
            config = json.load(f)
        # Declaring variables
        # TODO: Add variable for objectives
        # self.objectives = config['objectives']
        self.c1 = config['c1']
        self.c2 = config['c2']
        self.start_w = config['start_w']
        self.end_w = config['end_w']
        self.particle_num = config['particle_num']
        self.max_iterations = config['max_iterations']
        self.min_avg_velocity = config['min_avg_velocity']
        self.dimensions = config['dimensions']
        self.max = config['max']
        self.min = config['min']


class Particle:
    """
    Particle class
    """
    def __init__(self, dims, min_, max_):
        self.position = np.random.uniform(low=min_, high=max_, size=dims)
        self.position_fitness = zdt.ZDT1(self.position)
        self.velocity = np.random.uniform(low=min_, high=max_, size=dims)

        self.s_best_position = self.position.copy()
        self.p_best_position = self.position.copy()
        self.p_best_fitness = self.position_fitness.copy()

    def evaluate(self, pos):
        self.position = pos
        self.position_fitness = zdt.ZDT1(pos)

        if self.position_fitness < self.pBest_fitness:
            self.p_best_position = self.position
            self.p_best_fitness = self.position_fitness


class Swarm:
    """
    Swarm class
    """
    def apples(self):
        return


class Optimiser:
    """
    Swarm class
    """


class Archive:
    """
    Archive class
    """


class Solution:
    """
    Solution class
    """


def main():
    print("Main here")
    problem = Problem('config.json')
    print(problem.c1)
    return


if __name__ == '__main__':
    main()
