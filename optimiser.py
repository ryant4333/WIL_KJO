import sys
import random
import numpy as np
import math
import threading
import concurrent.futures
import time

sys.path.insert(1, "./src/")

import problem
import swarm
import hypercubes
import particle
import solution
import plot_graph

class SolutionContainer:
    def __init__(self):
        self.container = []
        self._lock = threading.Lock()
    
    def add(self, sol):
        with self._lock:
            self.container.append(sol)

def eval_thread(particle, objective, optimization_type, new_sols):
    sol = particle.evaluate(objective, optimization_type)
    new_sols.add(sol)

def move_thread(particle, c1, c2, weight, max_, min_):
    particle.move(c1, c2, weight, max_, min_)

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

    def run(self, workers=None, verbose=False):
        while True:
            self.iteration+=1
            if verbose:
                print(
                "ITERATION: ", self.iteration,
                " SOLS: ", self.hypercubes.sol_count,
                " AVG V: ", _get_avg_velocity(self.swarm.particles)
                )

            # evaluate particle positions
            new_sols = SolutionContainer()
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:               
                for particle in self.swarm.particles:
                    executor.submit(
                        eval_thread, 
                        particle, 
                        self.problem.objective, 
                        self.problem.optimization_type, 
                        new_sols
                    )
            
            updated = False
            for sol in new_sols.container:
                updated = self.hypercubes.update_bounds(sol)
            
            if updated:
                self.hypercubes.redo_dict(self.problem.optimization_type)
            
            for sol in new_sols.container:
                self.hypercubes.push_sol(sol, self.problem.optimization_type)
            
            #select each particles gbest
            for particle in self.swarm.particles:
                gbest = self.hypercubes.select_gbest()
                particle.s_best = gbest
            
            #move particles
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:  
                for particle in self.swarm.particles:
                    executor.submit(
                        move_thread,
                        particle,
                        self.problem.c1, 
                        self.problem.c2, 
                        self.weight, 
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
    
    if len(sys.argv) < 3:
        w = None
    else:
        w = int(sys.argv[2])

    sys.path.insert(1, d)
    config = d+"config.json"
    optimiser = Optimiser(config)
    start = time.perf_counter()
    optimiser.run(workers=w,verbose=True)
    end = time.perf_counter()
    print("RUNNING TIME: ", end - start, " seconds")
    plot_graph.plot(optimiser.problem.objective.__name__, optimiser, d)
