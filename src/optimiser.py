import problem
import swarm
import hypercubes
import particle
import solution

import random
import numpy as np
import math

class Optimiser:
    def __init__(self, config):
        self.problem = problem.Problem(config)
        self.swarm = swarm.Swarm(self.problem.particle_num,
            self.problem.min,
            self.problem.max)
        self.hypercubes = hypercubes.Hypercubes(self.problem.min,
            self.problem.max,
            self.problem.objectives,
            self.problem.cube_count)
        self.weight = random.uniform(self.problem.max_w, self.problem.min_w)
        self.iteration = 0
    
    def weightRegression(self, max, min):
        self.weight = random.uniform(max, min)
    
    def stop(self):
        if self.iteration >= self.problem.max_iterations:
            return True

        v = _get_avg_velocity(self.swarm.particles)

        if v < self.problem.min_avg_velocity:
            return True

        return False
    
def _get_avg_velocity(particles):
    v_sum = np.random.uniform(0, 0, len(particles[0].velocity))
    for particle in particles:
        v_sum = v_sum + particle.velocity

    v_average = v_sum / len(particles)
    print(v_average)
    v2 = sum(map(lambda x: x * x, v_average))
    v = math.sqrt(v2)
    return v

if __name__ == "__main__":
    swarm = swarm.Swarm(10, [0, 0], [1, 1])
    swarm.particles[0].velocity = np.array([1, 1])
    swarm.particles[1].velocity = np.array([2, 2])
    print(_get_avg_velocity(swarm.particles))
