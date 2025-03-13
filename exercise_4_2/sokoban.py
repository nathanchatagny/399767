import os
from sokoban_controller import SokobanController

# os.path.join for portable code (so it works on Mac/Windows/Linux)
path = os.path.join("levels", "level0.xsb")
sokoban = SokobanController(path)
sokoban.game_loop()