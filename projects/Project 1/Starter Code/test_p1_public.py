import unittest
import numpy as np

from p1 import LQ3K


class TestP1Public(unittest.TestCase):
    def test_simple_x(self):
        test = LQ3K(1)
        test.x(0)

        self.assertTrue(np.array_equal(test.get_unitary(), [[0, 1], [1, 0]]))
        self.assertTrue(np.array_equal(test.evolve([1, 0]), [0, 1]))
        self.assertEqual(test.simulate_run([1, 0]), 1)


if __name__ == "__main__":
    unittest.main()
