import sys
import random
import numpy as np
import math
import time
import multiprocessing
from functools import partial

sys.path.insert(1, "./src/")

import problem
import swarm
import hypercubes
import particle
import solution
import plot_graph

def eval_process(objective, particle):
    return particle.evaluate(objective)

class Optimiser:
    def __init__(self, config):
        self.problem = problem.Problem(config)
        self.swarm = swarm.Swarm(self.problem.particle_num,
            self.problem.min,
            self.problem.max, self.problem.swarm_distribution)
        self.hypercubes = hypercubes.Hypercubes(
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
            self.swarm = swarm.Swarm(self.problem.particle_num,
                self.problem.min,
                self.problem.max, self.problem.swarm_distribution)

        return False

    def run(self, verbose=False):
        #initalise process pool and functions
        cores = multiprocessing.cpu_count()
        if verbose:
            print("NUMBER OF CORES: ", cores)
            print("CREATING PROCESSES ... ", end = '')

        pool = multiprocessing.Pool(cores)
        if verbose:
            print("DONE")
            
        eval_func = partial(
            eval_process, 
            self.problem.objective
        )

        while True:
            self.iteration+=1
            if verbose:
                print(
                "ITERATION: ", self.iteration,
                " SOLS: ", self.hypercubes.sol_count,
                " AVG V: ", _get_avg_velocity(self.swarm.particles)
                )

            # evaluate particle positions
            new_sols = pool.map(eval_func, self.swarm.particles)

            # update pbest with new sols
            for i in range(len(self.swarm.particles)):
                self.swarm.particles[i].update_pbest(
                    new_sols[i], 
                    self.problem.optimization_type
                )
            
            updated = False
            for sol in new_sols:
                updated = self.hypercubes.update_bounds(sol)
            
            if updated:
                self.hypercubes.redo_dict(self.problem.optimization_type)
            
            for sol in new_sols:
                self.hypercubes.push_sol(sol, self.problem.optimization_type)
            
            #select each particles gbest
            for particle in self.swarm.particles:
                gbest = self.hypercubes.select_gbest()
                particle.s_best = gbest
            
            #calc particles veloctiy
            vs = []
            for particle in self.swarm.particles:
                vs.append(particle.calc_velocity(
                    self.problem.c1,
                    self.problem.c2, 
                    self.weight
                ))

            #move particles 
            for i in range(len(self.swarm.particles)):
                self.swarm.particles[i].move(
                    vs[i], 
                    self.problem.max, 
                    self.problem.min
                )

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
    d = sys.argv[1]
    if not d[-1] in ('/', '\\'):
        d+='/'

    sys.path.insert(1, d)
    config = d+"config.json"
    optimiser = Optimiser(config)
    start = time.perf_counter()
    optimiser.run(verbose=True)
    end = time.perf_counter()
    print("RUNNING TIME: ", end - start, " seconds")
    plot_graph.plot(optimiser.problem.objective.__name__, optimiser, d)
