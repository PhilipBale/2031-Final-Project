from time import sleep
from visual import *
import random
import string
import datetime
import atexit
import numpy as np

cell_width = 5
cell_height = 4
cell_scale = 200
padding = 20
inner_padding = 10

standard_color = color.black
hidden_color = color.red
found_color = color.green
path_color = color.cyan
robot_color = color.blue


object_marker = 10
visited_marker = 17
found_marker = 23

start_row = 3
start_col = 2

class DE2Robot(object):
    def __init__(self):
        super(DE2Robot, self).__init__()
        print "Robot created"

        self.row = start_row
        self.col = start_col




def draw_grid(grid): 
    rows, cols = grid.shape

    # Draw lines
    for y in range(rows + 1):
        curve(pos=[(padding, y * cell_scale + padding), (cols*cell_scale + padding, y * cell_scale + padding)], radius=1)
    for x in range(cols + 1):
        curve(pos=[(x * cell_scale + padding, padding), (x * cell_scale + padding, rows * cell_scale + padding)], radius=1)

def draw_cells(grid):
    rows, cols = grid.shape

    # Draw marked objects
    for i in range(rows):
        for j in range(cols):
            marker = grid[i,j]
            if marker == object_marker:
                draw_cell(i, j, hidden_color)
            elif marker == visited_marker:
                draw_cell(i, j, path_color)
            elif marker == found_marker:
                draw_cell(i, j, found_color)
            else:
                draw_cell(i, j, standard_color)
            draw_cell_label(i, j)

    # Draw robot
    draw_cell(robot.row, robot.col, robot_color)
    draw_cell_label(robot.row, robot.col)

def draw_cell_label(row, col):
    index = row * cell_width + col

    row_offset = row * cell_scale + padding + inner_padding + cell_scale / 2
    col_offset = col * cell_scale + padding + inner_padding + cell_scale / 2
    row_offset = scene.height - row_offset # Invert for cooridnate system

    labels[index].pos=(col_offset, row_offset)
    labels[index].text=("(" + str(col) + "," + str(row) + ")")

def draw_cell(row, col, color):
    index = row * cell_width + col

    row_offset = row * cell_scale + padding + inner_padding
    col_offset = col * cell_scale + padding + inner_padding

    boxes[index].pos=(col_offset + cell_scale / 2 - inner_padding, scene.height - (row_offset + cell_scale / 2 - inner_padding))
    boxes[index].color = color

def reset_grid(grid):
    robot.row = start_row
    robot.col = start_col

    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            grid[i,j] = False

def randomize_grid(grid):
    reset_grid(grid)
    num_objects = 3 + random.randint(0, 3)
    print "Randomizing with", num_objects, "objects"
    while num_objects > 0:
        rand_col = random.randint(0, cell_width - 2) #account for middle row
        rand_row = random.randint(0, cell_height - 1)
        if rand_col >= 2:
            rand_col += 1

        if (grid[rand_row, rand_col] == False):
            grid[rand_row, rand_col] = object_marker
            num_objects -= 1

    if not reachable(grid): # re-run if needed
        randomize_grid(grid)

def reachable(grid):
    rows, cols = grid.shape
    grid2 = np.mat([[0 for x in range(cell_width)] for x in range(cell_height)])
    grid2[:] = grid #deep copy so we can mangle

    traverse(grid2, start_row, start_col) # depth first recursive traversal

    # check if we hit traversed everything
    for i in range(rows):
        for j in range(cols):
            if grid2[i,j] == False or grid2[i,j] == object_marker:
                return False

    return True

def traverse(grid, row, col):
    spot_marked = 2

    if (row < 0 or row > cell_height - 1):
        return
    if (col < 0 or col > cell_width - 1):
        return

    if grid[row, col] == spot_marked or grid[row, col] == object_marker:
        if grid[row, col] == object_marker:
            grid[row, col] = spot_marked

        return

    grid[row, col] = spot_marked

    traverse(grid, row, col + 1)
    traverse(grid, row, col - 1) 
    traverse(grid, row + 1, col)
    traverse(grid, row - 1, col)

def quit(root):
    root.destroy()

def markRobotPosition():
    grid[robot.row,robot.col] = visited_marker

def finished():
    rows, cols = grid.shape

    for i in range(rows):
        for j in range(cols):
            if grid[i,j] == False:
                return False

    print "Finished!"
    sleep(10000)
    return True

def solve():
    depthFirstSearch(grid, robot.row, robot.col, True)

    draw_cells(grid)

    print "Solving finished!"

def depthFirstSearch(grid, row, col, base_case=False):
    if finished():
        return False
    print "Calling DFS for pos: ", row, ",", col
    if (row < 0 or row > cell_height - 1):
        print "Out of bounds row"
        return False
    elif (col < 0 or col > cell_width - 1):
        print "Out of bounds col"
        return False
    elif grid[row, col] == visited_marker:
        print "Already visited"
        return False
    elif grid[row, col] == found_marker:
        print "Already found"
        return False
    elif grid[row, col] == object_marker:
        print "New object!"
        #todo try find closest over multiple squares and make sure correct sonar side
        grid[row, col] = found_marker
        print "Object found! Pos: ", row, ",", col
        return False

    print "New position!"

    robot.row = row
    robot.col = col
 
    markRobotPosition()

    draw_cells(grid)
    sleep(.1)

    possible_moves = [(row, col+1), (row, col-1), (row+1, col), (row-1, col)]

    for move in possible_moves:
        sleep_time = 0
        if depthFirstSearch(grid, move[0], move[1]):
            sleep_time = .2
        #move back if needed
        robot.row = row
        robot.col = col
        draw_cells(grid)
        sleep(sleep_time)

    return True

def setup():
    scene.title='2031 Simulation'
    scene.width=(cell_width*cell_scale + padding * 2)
    scene.height=(cell_height * cell_scale + padding * 2)
    scene.center = (scene.width / 2, scene.height / 2, 0)

    print "Canvas width:", scene.width, "height:", scene.height
    scene.visible = True

    global grid
    grid = np.mat([[0 for x in range(cell_width)] for x in range(cell_height)])
    
    global labels
    labels = [label(box=False, opacity=0, color=color.white) for i in range(20)]

    global boxes
    boxes = [box(length=(cell_scale - inner_padding * 2), height=(cell_scale - inner_padding * 2)) for i in range(20)]

    global robot
    robot = DE2Robot()

print "Starting Simulation"
setup()
draw_grid(grid)

while True:
    rate(1) 
    randomize_grid(grid)
    draw_cells(grid)
    sleep(1)
    solve()

    sleep(500)
    



