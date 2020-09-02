import random
import numpy as np
from solution import Solution

class Particle:

    def __init__(self):
        self.p_best = None
        self.s_best = None
        self.x = []
        self.velocity = []

    def evaluate(self, objectives, optimization_type):
        """
        maybe updates p_best
        and returns new solution
        """
        obj = objectives(self.x)
        solution = Solution(self.x, obj)

        if self.p_best == None:
            self.p_best = solution

        dom_status = self.p_best.dominated(solution, optimization_type)
        
        if (dom_status == -1):
            self.p_best = solution
        elif(dom_status == 0):
            if random.random() > 0.5:
                self.p_best = solution
        
        return solution
  
    def move(self, c1, c2, w, maximum, minimum):
        if len(self.x) != len(maximum) or len(self.x) != len(minimum):
            raise TypeError("incorrect array size")
        
        inertia = np.array(self.velocity) * w
        cognitive = np.subtract(self.p_best.x, self.x) * c1 * random.uniform(0,1)
        social = np.subtract(self.s_best.x, self.x) * c2 * random.uniform(0,1)
        velocity = inertia + cognitive + social
        x = np.array(self.x) + velocity

        # check constraints
        for i in range(len(x)):
            if x[i] > maximum[i]:
                x[i] = maximum[i]
                velocity[i] *= -1
            elif x[i] < minimum[i]:
                x[i] = minimum[i]
                velocity *= -1
        
        self.x = x
        self.velocity = velocity

if __name__ == "__main__":
    particle = Particle()
    particle.p_best = Solution([1, 1], [1, 1])
    particle.s_best = Solution([1, 1], [5, 5])
    particle.x = [0, 0]
    particle.velocity = [0.5, 0.5]

    particle.move(1,1,1, [100,100], [-100, -100])
    print(particle.x)
    # looks like not random values but they are just linear
    
