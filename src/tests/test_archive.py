import unittest
import sys
import llist
sys.path.insert(1, "../")
from archive import Archive
from solution import Solution

class TestArchive(unittest.TestCase):

    # tests that a solution is pushed into archive
    def test_archive_empty_push(self):
        arch = Archive(10)
        sol1 = Solution([], [1, 1])
        arch.push(sol1, ["MAX", "MAX"])
        arch_len = len(arch.output())
        self.assertEqual(arch_len, 1)


    # tests both non-dominated solutions are added
    def test_archive_push_non_dominated(self):
        arch = Archive(10)
        sol1 = Solution([], [5, 5])
        sol2 = Solution([], [6, 4])
        arch.push(sol1, ["MAX", "MAX"])
        arch.push(sol2, ["MAX", "MAX"])
        arch_len = len(arch.output())
        self.assertEqual(arch_len, 2)

    # tests that dominated solution isnt added to archive
    # by checking len and that non-dom particle is still in
    def test_archive_push_dominated(self):
        arch = Archive(10)
        sol1 = Solution([], [5, 5])
        sol2 = Solution([], [1, 1])
        arch.push(sol1, ["MAX", "MAX"])
        arch.push(sol2, ["MAX", "MAX"])
        arch_len = len(arch.output())
        node = arch.output()[0]
        self.assertEqual(arch_len, 1)
        self.assertEqual(sol1, node)

    # tests that dominated solution in archive is removed
    def test_archive_remove_dominated(self):
        arch = Archive(10)
        sol1 = Solution([], [1, 1])
        sol2 = Solution([], [5, 5])
        arch.push(sol1, ["MAX", "MAX"])
        arch.push(sol2, ["MAX", "MAX"])
        arch_len = len(arch.output())
        node = arch.output()[0]
        self.assertEqual(arch_len, 1)
        self.assertEqual(sol2, node)

    # tests that multiple dominated solution in archive are removed
    def test_archive_remove_multi_dominated(self):
        arch = Archive(10)
        sol1 = Solution([], [1, 1])
        sol2 = Solution([], [2, 2])
        sol3 = Solution([], [5, 5])
        arch.push(sol1, ["MAX", "MAX"])
        arch.push(sol2, ["MAX", "MAX"])
        arch.push(sol3, ["MAX", "MAX"])
        arch_len = len(arch.output())
        node = arch.output()[0]
        self.assertEqual(arch_len, 1)
        self.assertEqual(sol3, node)

if __name__ == "__main__":
    unittest.main()