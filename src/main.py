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

        self.s_best_position = self.position
        self.p_best_position = self.position
        self.p_best_fitness = self.position_fitness

    def evaluate(self, new_position):
        """
        Updates p_best
        :param new_position: New particle position
        """
        self.position = new_position
        self.position_fitness = zdt.ZDT1(new_position)

        if self.position_fitness < self.p_best_fitness:
            self.p_best_position = self.position
            self.p_best_fitness = self.position_fitness


class Swarm:
    """
    Swarm class
    """
    eval_counter = 0  # TODO: implement with parallelisation

    def __init__(self, min_, max_, dims, p_num):
        particles = [Particle(min_=min_, max_=max_, dims=dims) for _ in range(p_num)]


class Optimiser:
    """
    Optimiser class
    """


class Archive:
    """
    Archive class
    """
    # TODO: Convert to linked-list
    # using an array instead of a linked-list for now
    # to reduce complexity.
    solutions = []

    def push(self, solution):
        """
        Push solution into solutions archive
        :param solution: Solution object
        """
        self.solutions.appened(solution)

    def output(self):
        """
        Displaying the solutions archive
        """
        print("Solutions:", self.solutions)


class Solution:
    """
    Solution class
    """
    # TODO: Need more information for this...
    x = []
    objectives = []


def main():
    config = Problem("config.json")
    test_swarm = Swarm(min_=config.min, max_=config.max, dims=config.particle_num)
    #Optimiser(test_swarm)
    return


if __name__ == '__main__':
    main()
