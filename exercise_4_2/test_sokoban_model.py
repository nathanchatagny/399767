import unittest
from exercise_4_3.sokoban_model import SokobanModel, Symbol, MoveResponse

class TestSokobanModel(unittest.TestCase):
    def test_level_completion_empty(self):
        """Test level completion with no boxes"""
        level_data = [
            "###",
            "#@#",
            "###"
        ]
        model = SokobanModel(level_data)
        # No boxes, so it's complete
        self.assertTrue(model.is_level_complete())

    def test_level_with_visible_box_incomplete(self):
        """Test level with visible box is not complete"""
        level_data = [
            "####",
            "#@$#",
            "#. #",
            "####"
        ]
        model = SokobanModel(level_data)
        self.assertFalse(model.is_level_complete())

    def test_level_with_uncovered_goal_but_no_visible_box_complete(self):
        """Test level with all boxes on goals is complete, even if there are uncovered goals"""
        level_data = [
            "#####",
            "#@*.#",
            "#####"
        ]
        model = SokobanModel(level_data)
        self.assertTrue(model.is_level_complete())

    def test_all_boxes_on_goals_complete(self):
        """Test level with all boxes on goals is complete"""
        level_data = [
            "#####",
            "#@**#",
            "#####"
        ]
        model = SokobanModel(level_data)
        self.assertTrue(model.is_level_complete())

    def test_level_completion_after_move(self):
        """Test level becomes complete after pushing the last visible box onto a goal"""
        # Simplified test case with clearer layout
        level_data = [
            "####",
            "#@$#",
            "#.##",
            "####"
        ]
        model = SokobanModel(level_data)
        
        # Check initial state
        self.assertFalse(model.is_level_complete())
        
        # Verify box and goal positions for debugging
        print("Initial state:")
        print(f"Boxes: {model.boxes}")
        print(f"Goals: {model.goals}")
        print(f"Player: {model.player}")
        
        # Move down to push box onto goal
        response = model.move(0, 1)
        
        # Verify state after move for debugging
        print("After move:")
        print(f"Move response: {response}")
        print(f"Boxes: {model.boxes}")
        print(f"Goals: {model.goals}")
        print(f"Player: {model.player}")
        
        # Check if level is complete
        self.assertEqual(response, MoveResponse.VALID)
        self.assertTrue(model.is_level_complete())
        
    def test_level_with_multiple_goals_and_boxes(self):
        """Test level with multiple goals and boxes is complete only when all boxes are on goals"""
        level_data = [
            "#######",
            "#@$...#",
            "#$$ ..#",
            "#######"
        ]
        model = SokobanModel(level_data)
        self.assertFalse(model.is_level_complete())
        
        # Reorganize the model manually to place all boxes on goals
        model.boxes.clear()
        goal_list = list(model.goals)
        for i in range(min(len(goal_list), 3)):  # We have 3 boxes in the test level
            model.boxes.add(goal_list[i])
            
        self.assertTrue(model.is_level_complete())

    # Add a new test with a more explicit scenario
    def test_manual_box_on_goal(self):
        """Test level completion by manually placing a box on goal"""
        level_data = [
            "####",
            "#@ #",
            "####"
        ]
        model = SokobanModel(level_data)
        
        # Add a goal and place a box on it
        goal_pos = (2, 1)
        model.goals.add(goal_pos)
        model.boxes.add(goal_pos)
        
        # Verify the level is complete
        self.assertTrue(model.is_level_complete())

if __name__ == '__main__':
    unittest.main()