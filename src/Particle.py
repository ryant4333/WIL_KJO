import numpy as np


class particle:
    def __init__(self, dims, min, max):     # init particle attributes
        self.position = np.random.uniform(low=min, high=max, size=dims)
        self.position_fitness = problem(self.position)
        self.velocity = np.random.uniform(low=min, high=max, size=dims)

        self.sBest_position = self.position.copy()
        self.pBest_position = self.position.copy()
        self.pBest_fitness = problem(self.position)

    def evaluate(self,pos):
        self.position = pos
        self.position_fitness = problem(pos)

        if self.position_fitness < self.pBest_fitness:
            self.pBest_position = self.position
            self.pBest_fitness = self.position_fitness

    def moveTo(self):
        optimise(self.position)





class problem:
    "Feed the particle position through to find fitness"

class optimise:
    "Moving the particle around the testspace"