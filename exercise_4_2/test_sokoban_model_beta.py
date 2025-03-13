import unittest
from sokoban import Sokoban

class TestSokobanModel(unittest.TestCase):
    def test_level_completed(self):
        """Test if the level completion check works correctly."""
        sokoban = Sokoban("test_level_completed.xsb")
        self.assertTrue(sokoban.is_level_completed())

    def test_level_not_completed(self):
        """Test a level where not all goals are covered by boxes."""
        sokoban = Sokoban("test_level_not_completed.xsb")
        self.assertFalse(sokoban.is_level_completed())

if __name__ == "__main__":
    unittest.main()