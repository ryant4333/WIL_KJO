import unittest
import sys
import os

sys.path.insert(1, "./src/")  # to import running in the test path
import plot_graph
import hypercubes
import solution


class TestPlotgraph(unittest.TestCase):

    def test_create_dir(self):
        test = "./tests/test"
        with self.assertRaises(FileExistsError):
            plot_graph.create_dir(test)

    def test_graph(self):
        test = "./tests/test/test_bad"
        test2 = "./tests/test/test_bad2"
        with self.assertRaises(ValueError):
            plot_graph.graph(test)
        with self.assertRaises(ValueError):
            plot_graph.graph(test2)

    def test_create_objectives_log(self):
        testdir = "./tests/test/"
        testbad = "./tests/test/test_bad"
        testgood = [[1,2,3], [1,2,3], [1,2,3], [1,2,3], [1,2,3]]
        with self.assertRaises(FileExistsError):
            plot_graph.create_objectives_log(testgood, testdir)
        with self.assertRaises(ValueError):
            os.remove("tests/test/objectives_log.txt")
            plot_graph.create_objectives_log(testbad, testdir)

    def test_create_sol_log(self):
        testdir = "./tests/test/"
        sol1 = solution.Solution([0, 1], [0, 1])
        sol2 = solution.Solution([1, 0], [1, 0])
        self.hypercubest = hypercubes.Hypercubes(10,10)
        self.hypercubest.bin_size = [1,2]
        self.hypercubest.push_sol(sol1, ["MIN", "MIN"])
        self.hypercubest.push_sol(sol2, ["MIN", "MIN"])

        with self.assertRaises(FileExistsError):
            plot_graph.create_sol_log(self.hypercubest.cube_dict,testdir,"test")



if __name__ == "__main__":
    unittest.main()
