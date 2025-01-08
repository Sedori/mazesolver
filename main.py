from graphics import Window, Line, Point, Cell, Maze

def main():
    win = Window(1024, 768)
    #line = Line(Point(50,100), Point(60,500))
    #win.draw_line(line, "pink")

    #c = Cell(50, 50, 100, 100, win)
    #c.left_wall = False
    #c.draw()
    #print(c.center_coordinates())

    #c = Cell(125,125, 200, 200, win)
    #c.right_wall = False
    #c.draw()
    #print(c.center_coordinates())

    #c = Cell(225, 225, 250, 250, win)
    #c.top_wall = False
    #c.draw()
    #print(c.center_coordinates())

    #c1 = Cell(300, 250, 192, 350, win)
    #c1.draw()
    #c1.draw_move(c, True)

    #Top-left cell (0,0)
    #cell1 = Cell(win)
    #cell1.draw(50, 50, 100, 100)

    #Top-right cell (1,0)
    #cell2 = Cell(win)
    #cell2.draw(100, 50, 150, 100)

    #Test drawing a line between adjacent cells
    #cell1.draw_move(cell2, False)  # should draw red line

    #Bottom-left cell (0,1)
    #cell3 = Cell(win)
    #cell3.draw(50, 100, 100, 150)

    #Test drawing vertical connection
    #cell1.draw_move(cell3, False)  # should draw red line

    #Let's also test the undo color
    #cell2.draw_move(cell3, True)   # should draw gray line

    maze = Maze(100, 100, 13, 11, 40, 40, win)

    maze._solve_r(0, 0)

    #maze._jail[0][0].draw_move(maze._jail[0][1])

    win.wait_for_close() #make sure this is at the end

if __name__ == "__main__":
    main()