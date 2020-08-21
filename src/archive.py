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


    def push(self, new_solution, optimization_type):
        """
        new_solution should be solution object

        for each solution in archive:
            Check if new solution dominates or is dominated

        """
        for sol in self.archive:
            if new_solution.fully_dominated(sol, ["MAX", "MAX"]):
                pass


        for each llist
        ll[5].fully_dominated(new_sol)
        self.archive.append(new_solution)
        pass
        #Is it empty
        #end when dominated
        #Cutout dominated solutions in archive
        #append


    def output():
        pass
        #returns archive

if __name__ == "__main__":
    sol1 = Solution([], [1,3])
    sol2 = Solution([], [1,2])
    sol3 = Solution([], [2,2])

    arch = Archive()