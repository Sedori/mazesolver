import unittest
from graphics import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._jail),
            num_cols,
        )
        self.assertEqual(
            len(m1._jail[0]),
            num_rows,
        )
    
    def test_break_entrance_and_exit(self):
    # Setup: initialize the maze and cell structures
        maze = Maze(x1=0, y1=0, num_rows=5, num_cols=5, cell_size_x=10, cell_size_y=10)
    
    # Assertions
        assert maze._jail[0][0].top_wall == False, "Entrance not broken correctly"
        assert maze._jail[maze.num_rows - 1][maze.num_cols - 1].bottom_wall == False, "Exit not broken correctly"
    
    # Include any further checks as necessary

    def test_all_is_reset(self):

        maze = Maze(0, 0, 5, 5, 10, 10)

        all_reset = True

        for i in range(maze.num_cols):
            for j in range(maze.num_rows):
                if maze._jail[i][j].visited:
                    print(f"This is visited: ({i}, {j})")
                    all_reset = False
                    break
        
        self.assertTrue(all_reset)

        


if __name__ == "__main__":
    unittest.main()