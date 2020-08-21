class Archive:
    """
    Archive class
    """
    # TODO: Convert to linked-list
    # using an array instead of a linked-list for now
    # to reduce complexity.
    solutions = []

    def push(self, solution):
        """
        Push solution into solutions archive
        :param solution: Solution object
        """
        self.solutions.appened(solution)

    def output(self):
        """
        Displaying the solutions archive
        """
        print("Solutions:", self.solutions)
