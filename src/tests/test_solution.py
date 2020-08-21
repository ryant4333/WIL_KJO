# needs to run from test file
import unittest
import sys
sys.path.insert(1, "../") # to import running in the test path
from solution import Solution


class TestSolution(unittest.TestCase):

    def test_fully_dominated_max(self):
        sol1 = Solution([], [1, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.fully_dominated(sol2, ["MAX", "MAX"])
        opposite = sol2.fully_dominated(sol1, ["MAX", "MAX"])
        self.assertEqual(boolean, True)
        self.assertEqual(opposite, False)
    
    def test_fully_dominated_min(self):
        sol1 = Solution([], [1, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.fully_dominated(sol2, ["MIN", "MIN"])
        opposite = sol2.fully_dominated(sol1, ["MIN", "MIN"])
        self.assertEqual(boolean, False)
        self.assertEqual(opposite, True)
    
    def test_fully_dominated_max_one_difference(self):
        sol1 = Solution([], [5, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.fully_dominated(sol2, ["MAX", "MAX"])
        opposite = sol2.fully_dominated(sol1, ["MAX", "MAX"])
        self.assertEqual(boolean, True)
        self.assertEqual(opposite, False)
    
    def test_fully_dominated_min_one_difference(self):
        sol1 = Solution([], [5, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.fully_dominated(sol2, ["MIN", "MIN"])
        opposite = sol2.fully_dominated(sol1, ["MIN", "MIN"])
        self.assertEqual(boolean, False)
        self.assertEqual(opposite, True)

if __name__ == "__main__":
    unittest.main()