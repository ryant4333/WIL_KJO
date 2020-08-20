import solution as solutions


class Particle:

    def __init__(self, pos):
        self.p_best = None
        self.s_best = None
        self.x = pos
        self.velocity = None

    def evaluate(self, objectives, optimization_type):
        """
      maybe updates p_best
      and returns new solution
      """
        obj = objectives(self.x)
        solution = solutions.Solution(self.x, obj)

        if self.p_best.fully_dominated(solution, optimization_type):
            self.p_best = solution

        return solution

    def move(self, c1, c2, w, maximum, minimum):
        pass
