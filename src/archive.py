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
    def __init__(self, limit):
        #Archive is singly linked list, can be easily changed to doubly
        self.archive = llist.sllist()
        self.limit = limit

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
        
        if len(self.archive) >= self.limit:
            print("Limit hit! To be Implemented")
            self.archive.append(new_solution)

            """ 
            only look through <10> solutions at a time
            Find worst non_dominated solution
            replace with new solution
            """
            # print("Limit hit")
            # #All solutions including new are non dominated
            # self.archive.rotate(3)
            # worst_node = new_solution
            # current_node = self.archive.first.value
            # for i in range(3):

            # print(max_node)
            # print(current_node)
        else:
            self.archive.append(new_solution)
        
        return

    def non_dom_comp(self, sol1, sol2, optimization_type):
        # Returns the better non dominated solution
        sol1_count = 0
        sol2_count = 0
        for i in range(len(optimization_type)):
            if optimization_type[i] == "MAX":
                sol1_count += sol1.objectives[i]
                sol2_count += sol2.objectives[i]
            if optimization_type[i] == "MIN":
                sol1_count -= sol1.objectives[i]
                sol2_count -= sol2.objectives[i]
        if sol1_count > sol2_count:
            return sol1
        else:
            return sol2


    def output(self):
        #Currently returning a linked list
        #Should it return an array once done?
        print(self.archive.size)
        return self.archive

    def write_out(self):
        f_handler = open("archive_output.txt", "a")
        for i in range(len(self.archive)):
            line = "{}, {}\n".format(self.archive[i].x, self.archive[i].objectives)
            f_handler.write(line)
        f_handler.close()


if __name__ == "__main__":
    sol1 = Solution([], [7,3,5])  #15
    sol2 = Solution([], [8,2,4])  #14
    sol3 = Solution([], [9,1,6])  #16
    sol4 = Solution([], [5,5,8])  #18
    sol5 = Solution([], [6,4,1])  #11

    arch = Archive(3)

    arch.push(sol1, ["MAX", "MAX", "MAX"])
    arch.push(sol2, ["MAX", "MAX", "MAX"])
    arch.push(sol3, ["MAX", "MAX", "MAX"])
    arch.push(sol4, ["MAX", "MAX", "MAX"])
    arch.push(sol5, ["MAX", "MAX", "MAX"])

    print(arch.output())
    
    # arch.write_out()