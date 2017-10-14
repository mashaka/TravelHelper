"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Tests for generator.py module
"""
import unittest

from algo import generate_trips

class TestUtils(unittest.TestCase):
    """
    Tests for generator.py module
    """

    def setUp(self):
        pass

    def test_generate_trips(self):
        """
        Tests only correctness of an output json for generate.generate_trips function
        """
        trips = generate_trips([], [])
        self.assertEqual(len(trips), 2)


if __name__ == '__main__':
    unittest.main()
