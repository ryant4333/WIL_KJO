import llist
#Documentation for llist: https://ajakubek.github.io/python-llist/index.html
from solution import Solution

"""
Init archive in optimiser
particles push evaluated solutions, {obj}
check against all archive values
unless dominated then end

Potential changes:
    Fast sort archive
    Current implementation of sol.fully_dominated needs to be run twice?
"""

class Archive:
    def __init__(self):
        #Archive is singly linked list, can be easily changed to doubly
        self.archive = llist.sllist()

    #def push(self, new_solution, optimization_type):
    #Optimization_type currently hard coded
    def push(self, new_solution):
        """
        new_solution should be solution object

        for each solution in archive:
            Check if new solution dominates or is dominated

        """
        for sol in self.archive:
            if new_solution.fully_dominated(sol, ["MAX", "MAX"]):
                #The new solution is dominated by sol in archive
                print(new_solution, " Is Dominated by ", sol)
                return
            #if new_solution.fully_dominated(sol, ["MAX", "MAX"]):
                # node = self.arch
                # self.archive.remove(self.archive)
        print("Adding solution to list: ", new_solution)
        self.archive.append(new_solution)    




    def output():
        pass
        #returns archive

if __name__ == "__main__":
    sol1 = Solution([], [1,3])
    sol2 = Solution([], [1,2])
    sol3 = Solution([], [2,2])

    arch = Archive()

    arch.push(sol1)
    arch.push(sol2)
    arch.push(sol3)