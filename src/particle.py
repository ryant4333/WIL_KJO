import random
import numpy as np
from solution import Solution

class Particle:

    def __init__(self):
        self.p_best = None
        """Position of the particles personal best."""
        self.s_best = None
        """Position of the global best (taken from hypercubes class)."""
        self.x = []
        """Current position of the particle."""
        self.velocity = []
        """Inertia of particle."""

    def evaluate(self, objectives: callable) -> Solution:
        """
        Gets objectives based on the particles current position. Uses these 
        objectives and the particles position to return a new solution.
        """
        obj = objectives(self.x)
        solution = Solution(self.x, obj)        
        return solution
  
    def move(self, velocity: list, maximum: list, minimum: list) -> None:
        """Changes the position of the particle, maintains search space 
        constraints, and saves velocity."""
        if len(self.x) != len(maximum) or len(self.x) != len(minimum):
            raise TypeError("incorrect array size")
        
        x = np.array(self.x) + velocity

        # check constraints
        for i in range(len(x)):
            if x[i] > maximum[i]:
                x[i] = maximum[i]
                velocity[i] *= -1
            elif x[i] < minimum[i]:
                x[i] = minimum[i]
                velocity[i] *= -1
        
        self.x = x
        self.velocity = velocity
    
    def calc_velocity(self, c1: float, c2: float, w: float) -> list:
        """Calculates the velocity of the particle with cognitive, social and 
        inertia weight."""
        inertia = np.array(self.velocity) * w
        cognitive = np.subtract(self.p_best.x, self.x) * c1 * random.uniform(0,1)
        social = np.subtract(self.s_best.x, self.x) * c2 * random.uniform(0,1)
        velocity = inertia + cognitive + social
        return velocity
    
    def update_pbest(self, solution: Solution, optimization_type: list) -> None:
        """Determines if new solution fully dominates personal best. If it does,
        it becomes new personal best. If new solution is not fully dominated by
        personal best, it updates it with a %50 chance."""
        if self.p_best == None:
            self.p_best = solution

        dom_status = self.p_best.dominated(solution, optimization_type)
        
        if (dom_status == -1):
            self.p_best = solution
        elif(dom_status == 0):
            if random.random() > 0.5:
                self.p_best = solution

if __name__ == "__main__":
    pass
    
