class Solution:
    def __init__(self, x, objectives):
        """Objectives array of floats that specify pos fitness"""
        self.x = x
        self.objectives = objectives

    def __repr__(self):
        #repr so print function prints objects for testing purposes
        return "<Solution x:{}, obj:{}>".format(self.x, self.objectives)

    # returns true if the inputed solution can fully dominate
    def fully_dominated(self, solution, optimization_type):
        for i in range(len(self.objectives)):
            if optimization_type[i] == "MAX":
                if self.objectives[i] > solution.objectives[i]:
                    return False
            elif optimization_type[i] == "MIN":
                if self.objectives[i] < solution.objectives[i]:
                    return False
        return True

if __name__ == "__main__":
    sol1 = Solution([], [1,3])
    sol2 = Solution([], [1,2])

    print(sol1.fully_dominated(sol2, ["MAX", "MAX"])) #should return true