import random
import time
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("I'm a Window")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
    
    def close(self):
        self.__running = False

class Point:
    def __init__(self, x, y):
        self.horizontal = x
        self.vertical = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color="red"):
        canvas.create_line(self.p1.horizontal, self.p1.vertical, self.p2.horizontal, self.p2.vertical, fill=fill_color, width=3)


class Cell:
    def __init__(self, win=None):
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False
    
    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line)
        if self.bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line)
        if self.top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line)
        if self.right_wall:
            line = Line(Point(self._x2, self._y2), Point(self._x2, self._y1))
            self._win.draw_line(line)

        # janky if no walls    
        if not self.left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "white")
        if not self.bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "white")
        if not self.top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "white")
        if not self.right_wall:
            line = Line(Point(self._x2, self._y2), Point(self._x2, self._y1))
            self._win.draw_line(line, "white")
    
    
    def center_coordinates(self):
        mid_x = (self._x2 + self._x1) / 2
        mid_y = (self._y2 + self._y1) / 2
        return mid_x, mid_y

    
    def draw_move(self, to_cell, undo=False):
        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        point_1 = self.center_coordinates()
        point_2 = to_cell.center_coordinates()
        line = Line(Point(point_1[0], point_1[1]), Point(point_2[0], point_2[1]))
        self._win.draw_line(line, fill_color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._jail = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
           self.seed = seed
           random.seed(seed)

        self._create_jail()
        self._break_walls(0,0)
        self._break_entrance_and_exit()
        self._reset_cells_visited()
        
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        
                
        
    def _create_jail(self):
        for i in range(self.num_cols):
            col_jail = []
            for j in range(self.num_rows):
                col_jail.append(Cell(self._win))
            self._jail.append(col_jail)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)



    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x_coord_1 = (self.cell_size_x * i) + self.x1
        y_coord_1 = (self.cell_size_y * j) + self.y1
        y_coord_2 = y_coord_1 + self.cell_size_y
        x_coord_2 = x_coord_1 + self.cell_size_x
        self._jail[i][j].draw(x_coord_1, y_coord_1, x_coord_2, y_coord_2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._jail[0][0].top_wall = False
        self._draw_cell(0,0)
        self._jail[-1][-1].bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)
    
    def _break_walls(self, i, j):
        if self._jail[i][j].visited == False:
            self._jail[i][j].visited = True
            while True:
                to_visit = []
                to_visit.append((i-1, j)) # up (actually left?)
                to_visit.append((i+1, j)) # down (actually right?)
                to_visit.append((i, j-1)) # left (actually up?)
                to_visit.append((i, j+1)) # right (actually down?)
                directions = []
                for visit in to_visit:
                    new_i, new_j = visit
                    if self._is_valid_cell(new_i, new_j) and not self._jail[new_i][new_j].visited:
                        directions.append(visit)
                if not directions:
                    return
                chosen_one = random.choice(directions)
                new_i, new_j = chosen_one
                if new_i < i: # moving upwards (actually left?)
                    self._jail[i][j].left_wall = False
                    self._jail[new_i][new_j].right_wall = False
                elif new_i > i: # moving downwards (right?)
                    self._jail[i][j].right_wall = False
                    self._jail[new_i][new_j].left_wall = False
                elif new_j < j: # moving left (up?)
                    self._jail[i][j].top_wall = False
                    self._jail[new_i][new_j].bottom_wall = False
                elif new_j > j: # moving right (down?)
                    self._jail[i][j].bottom_wall = False
                    self._jail[new_i][new_j].top_wall = False
                self._break_walls(new_i, new_j)
    
    def _is_valid_cell(self, i, j):
        return i >= 0 and i < self.num_cols and j >= 0 and j < self.num_rows
    
    def _can_move_between(self, i, j, i2, j2):
        if i2 < i: # left
            print(f"Cell ({i2}, {j2}) is being checked for its Left Wall")
            if self._jail[i][j].left_wall == False:
                return True
        elif i2 > i: # right
            print(f"Cell ({i2}, {j2}) is being checked for its Right Wall")
            if self._jail[i][j].right_wall == False:
                return True
        elif j2 < j: # up
            print(f"Cell ({i2}, {j2}) is being checked for its Top Wall")
            if self._jail[i][j].top_wall == False:
                return True
        elif j2 > j: # down
            print(f"Cell ({i2}, {j2}) is being checked for its Bottom Wall")
            if self._jail[i][j].bottom_wall == False:
                return True
        return False

    

    def _can_move_to(self, i, j):
        if self._is_valid_cell(i, j) and not self._jail[i][j].visited:
            pass
    
    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._jail[i][j].visited = False
    

    def _solve_r(self, i, j):
        print("I have started:")
        self._animate()
        self._jail[i][j].visited = True
        print(f"Cell ({i}, {j}) has been visited")
        if self._jail[i][j] == self._jail[self.num_cols - 1][self.num_rows - 1]:
            print("I have somehow found the exit")
            return True
        
        to_visit = [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]
        random.shuffle(to_visit)
        directions = []
        for visit in to_visit:
            new_i, new_j = visit
            print(f"I will visit Cell ({new_i}, {new_j})")
            if self._is_valid_cell(new_i, new_j) and self._jail[new_i][new_j].visited == False:
                print(f"Cell ({new_i}, {new_j}) may be attempted to be visited")
                directions.append(visit)
        if not directions:
            print(f"There are no directions available for me")
            return
        for viable in directions:
            new_i, new_j = viable
            print(f"I will now check if it is viable to move to Cell ({new_i}, {new_j})")
            if self._can_move_between(i, j, new_i, new_j):
                self._jail[i][j].draw_move(self._jail[new_i][new_j])
                if self._solve_r(new_i, new_j):
                    return True
                self._jail[i][j].draw_move(self._jail[new_i][new_j], True)