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
        ll_pos = 0

        for sol in self.archive:
            dom_status = new_solution.dominated(sol, optimization_type)

            if dom_status == -1:
                #Self/new_solution is dominated, end
                return
            elif dom_status == 1:
                #Archive sol is dominated by new_solution
                node = self.archive.nodeat(ll_pos)
                self.archive.remove(node)
                ll_pos -= 1
                #As archive is shorter pos needs to be shorter
            elif dom_status == 0:
                pass
            else:
                raise ValueError("Dom status has incorrect value:", dom_status)
            ll_pos += 1
        
        self.archive.append(new_solution)
        return


    def output(self):
        return self.archive

if __name__ == "__main__":
    sol1 = Solution([], [1,3])
    sol2 = Solution([], [1,2])
    sol3 = Solution([], [2,2])
    sol4 = Solution([], [5,5])
    sol5 = Solution([], [6,4])

    arch = Archive()

    arch.push(sol1, ["MAX", "MAX"])
    arch.push(sol2, ["MAX", "MAX"])
    arch.push(sol3, ["MAX", "MAX"])
    arch.push(sol4, ["MAX", "MAX"])
    arch.push(sol5, ["MAX", "MAX"])

    print(arch.output())