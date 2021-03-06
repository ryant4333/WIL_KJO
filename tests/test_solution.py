# needs to run from test file
import unittest
import sys
sys.path.insert(1, "./src/") # to import running in the test path
from solution import Solution


class TestSolution(unittest.TestCase):    

    def test_dominated_max(self):
        sol1 = Solution([], [1, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.dominated(sol2, ["MAX", "MAX"])
        opposite = sol2.dominated(sol1, ["MAX", "MAX"])
        self.assertEqual(boolean, -1)
        self.assertEqual(opposite, 1)
    
    def test_dominated_min(self):
        sol1 = Solution([], [1, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.dominated(sol2, ["MIN", "MIN"])
        opposite = sol2.dominated(sol1, ["MIN", "MIN"])
        self.assertEqual(boolean, 1)
        self.assertEqual(opposite, -1)
    
    def test_dominated_0(self):
        sol1 = Solution([], [6, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.dominated(sol2, ["MAX", "MAX"])
        opposite = sol2.dominated(sol1, ["MAX", "MAX"])
        self.assertEqual(boolean, 0)
        self.assertEqual(opposite, 0)
    
    def test_dominated_max_one_difference(self):
        sol1 = Solution([], [5, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.dominated(sol2, ["MAX", "MAX"])
        opposite = sol2.dominated(sol1, ["MAX", "MAX"])
        self.assertEqual(boolean, -1)
        self.assertEqual(opposite, 1)
    
    def test_dominated_min_one_difference(self):
        sol1 = Solution([], [5, 1])
        sol2 = Solution([], [5, 5])
        boolean = sol1.dominated(sol2, ["MIN", "MIN"])
        opposite = sol2.dominated(sol1, ["MIN", "MIN"])
        self.assertEqual(boolean, 1)
        self.assertEqual(opposite, -1)
    
    def test_dominated_solution_error(self):
        sol1 = Solution([], [5, 1])
        sol2 = Solution([], [5, 5, 5])
        with self.assertRaises(TypeError):
            boolean = sol1.dominated(sol2, ["MIN", "MIN"])
    
    def test_dominated_optimization_type_size_error(self):
        sol1 = Solution([], [5, 1])
        sol2 = Solution([], [5, 5])
        with self.assertRaises(TypeError):
            boolean = sol1.dominated(sol2, ["MIN"])
    
    def test_dominated_optimization_type_value_error(self):
        sol1 = Solution([], [5, 1])
        sol2 = Solution([], [5, 5])
        with self.assertRaises(TypeError):
            boolean = sol1.dominated(sol2, ["MIN", "AXE"])

    def test_non_dominated_same_solution(self):
        sol1 = Solution([], [5, 5])
        sol2 = Solution([], [5, 5])
        boolean = sol1.dominated(sol2, ["MIN", "MIN"])
        opposite = sol2.dominated(sol1, ["MIN", "MIN"])
        self.assertEqual(boolean, 1)
        self.assertEqual(opposite, 1)
        

if __name__ == "__main__":
    unittest.main()
