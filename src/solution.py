import numpy as np

class Solution:
    def __init__(self, x, objectives):
        self.x = np.array(x)
        """Holds solution position."""
        self.objectives = np.array(objectives)
        """Objectives array of floats that specify pos fitness"""

    def __repr__(self):
        #repr prints objects for testing purposes
        return "<Solution x:{}, obj:{}>".format(self.x, self.objectives)

    
    # returns 1 if self dominates, -1 is param solution dominates 
    # and 0 if neither dominate 
    def dominated(self, solution, optimization_type: list) -> int:
        """Determines which solution dominates which. Returns 1 if self 
        instance dominates, -1 if param sol dominates and 0 if neither. Unlikely
        edge case where both solutions equal each other returns 1"""
        if len(self.objectives) != len(solution.objectives):
            raise TypeError("solutions have different objective sizes")
        if len(self.objectives) != len(optimization_type):
            raise TypeError("optimization_type has different size")
        
        x = 0
        y = 0

        for i in range(len(self.objectives)):
            if self.objectives[i] == solution.objectives[i]:
                continue
            if optimization_type[i] == "MAX":
                if self.objectives[i] > solution.objectives[i]:
                    x+=1
                else:
                    y+=1
            elif optimization_type[i] == "MIN":
                if self.objectives[i] < solution.objectives[i]:
                    x+=1
                else:
                    y+=1
            else:
                raise ValueError("optimization_type has incorrect value at " + i)
        
        if x > 0 and y > 0:
            return 0
        if x > 0:
            return 1
        if y > 0:
            return -1
        return 1
if __name__ == "__main__":
    sol1 = Solution([], [1,1])
    sol2 = Solution([], [1,1])
    print(sol1.dominated(sol2, ["MAX", "MAX"]))