class Particle:

  def __init__(self):
      self.p_best = None
      self.s_best = None
      self.x = None
      self.velocity = None


  def evaluate(self, objectives, optimization_type):
      """
      maybe updates p_best
      and returns new solution
      """
      obj = objectives(self.x)
      solution = Solution(self.x, obj)
      
      if(self.p_best.fully_dominated(solution, optimization_type) == True):
      	self.p_best = solution
      
      return solution
  
  def move(self, c1, c2, w, maximum, minimum):
    pass