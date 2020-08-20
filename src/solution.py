class Solution:
	def __init__(self, x, objectives):
        self.x = x
        self.objectives = objectives
    def full_dominated(self, solution, optimization_type):
        for i in range(len(self.objectives)):
            if(optimization_type[i] == "MAX"):
                if(self.objectives[i] > solution.objectives[i]):
                    return False
            else if(optimization_type[i] == "MIN"):
                if(self.objectives[i] < solution.objectives[i]):
                    return False
        return True