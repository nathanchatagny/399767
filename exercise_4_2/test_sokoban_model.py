import unittest

from sokoban_model import MoveResponse, SokobanModel, Symbol

SIMPLE_LEVEL = """######
#-$-.#
#-$-.#
#-@--#
######""".splitlines()

# Level where one box is already on a goal
PARTIAL_COMPLETE_LEVEL = """######
#-$-.#
#-*-.#
#-@--#
######""".splitlines()

# Using a very simple level for completion test
# Just one box that's already on a goal
COMPLETE_LEVEL = """###
#*#
#@#
###""".splitlines()


class TestSokobanModel(unittest.TestCase):
    def test_player_can_move_into_empty_space(self):
        model = SokobanModel(SIMPLE_LEVEL)
        self.assertEqual(model.move(1, 0), MoveResponse.VALID)

    def test_player_cannot_move_into_wall(self):
        model = SokobanModel(SIMPLE_LEVEL)
        self.assertEqual(model.move(0, 1), MoveResponse.INVALID_WALL)

    def test_player_can_move_box_into_empty_space(self):
        model = SokobanModel(SIMPLE_LEVEL)
        self.assertEqual(model.move(1, 0), MoveResponse.VALID)
        self.assertEqual(model.move(0, -1), MoveResponse.VALID)
        self.assertEqual(model.move(-1, 0), MoveResponse.VALID)

    def test_player_cannot_move_box_into_box(self):
        model = SokobanModel(SIMPLE_LEVEL)
        self.assertEqual(model.move(0, -1), MoveResponse.INVALID_BOX)

    def test_player_cannot_move_box_into_wall(self):
        model = SokobanModel(SIMPLE_LEVEL)
        self.assertEqual(model.move(1, 0), MoveResponse.VALID)
        self.assertEqual(model.move(0, -1), MoveResponse.VALID)
        self.assertEqual(model.move(-1, 0), MoveResponse.VALID)
        self.assertEqual(model.move(-1, 0), MoveResponse.INVALID_BOX)

    # Testing an incomplete level ensures the game doesn't end prematurely
    def test_level_not_complete(self):
        model = SokobanModel(SIMPLE_LEVEL)
        self.assertFalse(model.is_level_complete())

    # Testing a partially complete level to verify the function handles mixed states correctly
    def test_level_partially_complete(self):
        model = SokobanModel(PARTIAL_COMPLETE_LEVEL)
        self.assertFalse(model.is_level_complete())

    # Testing a fully complete level to confirm victory condition is detected
    # Using a minimal level to simplify testing
    def test_level_complete(self):
        model = SokobanModel(COMPLETE_LEVEL)
        
        # Print debug information to understand what's happening
        print("Goals:", model.goals)
        print("Boxes:", model.boxes)
        print("All goals covered?", all(goal in model.boxes for goal in model.goals))
        
        self.assertTrue(model.is_level_complete())

    # Testing that moving a box onto a goal properly updates the completion status
    # This test simulates actual gameplay to ensure the game can be completed through player actions
    def test_completing_level_through_moves(self):
        # Create a custom level with a simpler path to completion for testing
        custom_level = """#####
#@$.#
#####""".splitlines()
        
        model = SokobanModel(custom_level)
        
        # Verify level is not complete at start
        self.assertFalse(model.is_level_complete())
        
        # Push the box onto the goal
        self.assertEqual(model.move(1, 0), MoveResponse.VALID)
        
        # Debug information
        print("After move - Goals:", model.goals)
        print("After move - Boxes:", model.boxes)
        
        # Now the level should be complete
        self.assertTrue(model.is_level_complete())


if __name__ == "__main__":
    unittest.main()