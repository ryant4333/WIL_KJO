import numpy as np
import zdt_test as zdt


class Particle:
    def __init__(self, dims, min_, max_):     # init particle attributes
        self.position = np.random.uniform(low=min_, high=max_, size=dims)
        self.position_fitness = zdt.ZDT1(self.position)
        self.velocity = np.random.uniform(low=min_, high=max_, size=dims)

        self.sBest_position = self.position.copy()
        self.pBest_position = self.position.copy()
        self.pBest_fitness = self.position_fitness.copy()

    def evaluate(self, pos):
        self.position = pos
        self.position_fitness = zdt.ZDT1(pos)

        if self.position_fitness < self.pBest_fitness:
            self.pBest_position = self.position
            self.pBest_fitness = self.position_fitness

