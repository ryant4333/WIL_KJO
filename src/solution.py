class Solution:
    def __init__(self, x, objectives):
        self.x = x
        self.objectives = objectives

    # returns true if the inputed solution can fully dominate
    def fully_dominated(self, solution, optimization_type):
        if len(self.objectives) != len(solution.objectives):
            raise TypeError("solutions have different objective sizes")
        if len(self.objectives) != len(optimization_type):
            raise TypeError("optimization_type has different size")

        for i in range(len(self.objectives)):
            if optimization_type[i] == "MAX":
                if self.objectives[i] > solution.objectives[i]:
                    return False
            elif optimization_type[i] == "MIN":
                if self.objectives[i] < solution.objectives[i]:
                    return False
            else:
                raise TypeError("optimization_type has incorrect type at " + i)
        return True

if __name__ == "__main__":
    sol1 = Solution([], [1,3])
    sol2 = Solution([], [1,2])

    print(sol1.fully_dominated(sol2, ["MAX", "MAX"])) #should return true