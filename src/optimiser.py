import problem
import swarm
import hypercubes
import particle
import solution
import zdt_test

import random
import numpy as np
import math

class Optimiser:
    def __init__(self, config, ZDT=None):
        self.problem = problem.Problem(config)
        if ZDT != None:
            self.problem.import_zdt(ZDT)
        self.swarm = swarm.Swarm(self.problem.particle_num,
            self.problem.min,
            self.problem.max)
        self.hypercubes = hypercubes.Hypercubes(self.problem.min,
            self.problem.max,
            self.problem.objective,
            self.problem.cube_count,
            self.problem.solution_count)
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

    def run(self):
        while True:
            self.iteration+=1
            print("ITERATION: ", self.iteration, " AVG V: ", _get_avg_velocity(self.swarm.particles))

            # print("EVAL")
            # evaluate particle positions
            for particle in self.swarm.particles:
                sol = particle.evaluate(self.problem.objective, self.problem.optimization_type) # this updates pbest
                self.hypercubes.push_sol(sol, self.problem.optimization_type)
            
            # print("GBEST")
            #select each particles gbest
            for particle in self.swarm.particles:
                gbest = self.hypercubes.select_gbest()
                particle.s_best = gbest
            
            # print("MOVE")
            #move particles
            for particle in self.swarm.particles:
                particle.move(self.problem.c1, self.problem.c2, self.weight, 
                    self.problem.max, self.problem.min)

            # print("FRONT")
            # self.hypercubes.output()
            
            # print("STOP?")

            if self.stop():
                break

def _get_avg_velocity(particles):
    v_sum = np.random.uniform(0, 0, len(particles[0].velocity))
    for particle in particles:
        v_sum = v_sum + particle.velocity

    v_average = v_sum / len(particles)
    v2 = sum(map(lambda x: x * x, v_average))
    v = math.sqrt(v2)
    return v

if __name__ == "__main__":
    optimiser = Optimiser("config.json", zdt_test.ZDT1)
    optimiser.run()
    optimiser.hypercubes.draw_front()