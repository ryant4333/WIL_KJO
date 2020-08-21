import llist

"""
Init archive in optimiser
particles push evaluated solutions, {obj}
check against all archive values
unless dominated then end
"""
class Archive:
    def __init__(self):
        self.archive = llist.sllist()


    def push(self, eval_obj):
        
        pass
        #Is it empty
        #end when dominated
        #Cutout dominated solutions in archive
        #append


    def output():
        pass
        #returns archive

if __name__ == "__main__":
    arch = Archive()
    print(arch.archive)