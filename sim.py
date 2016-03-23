from time import sleep
from Tkinter import *
import random
import string
import datetime
import atexit
import numpy as np

cell_width = 5
cell_height = 4
cell_scale = 200
padding = 20
inner_padding = 5
hidden_color = "red"
found_color = "green"
robot_color = "blue"

object_marker = 10

start_row = 3
start_col = 2

robot_pos = (start_row, start_col)

def draw_grid(grid): 

    print "Drawing Grid"
    rows, cols = grid.shape
    print "Width:", canvas['width'], "Height:", canvas['height']
    print "Rows:", rows, ", Cols:", cols

    # Draw lines
    for y in range(rows + 1):
        canvas.create_line(padding, y * cell_scale + padding, cols*cell_scale + padding, y * cell_scale + padding)
    for x in range(cols + 1):
        canvas.create_line(x * cell_scale + padding, padding, x * cell_scale + padding, rows * cell_scale + padding)


    # Draw marked objects
    for i in range(rows):
        for j in range(cols):
            if (grid[i,j] == object_marker):
                draw_cell(i, j, hidden_color)
            draw_cell_label(i, j)

    # Draw robot
    draw_cell(robot_pos[0], robot_pos[1], robot_color)
    draw_cell_label(robot_pos[0], robot_pos[1])

def draw_cell_label(row, col):
    row_offset = row * cell_scale + padding + inner_padding + cell_scale / 2
    col_offset = col * cell_scale + padding + inner_padding + cell_scale / 2
    canvas.create_text(col_offset, row_offset, text=("(" + str(col) + "," + str(row) + ")"))

def draw_cell(row, col, color):
    row_offset = row * cell_scale + padding + inner_padding
    col_offset = col * cell_scale + padding + inner_padding

    canvas.create_rectangle(col_offset, row_offset, col_offset + cell_scale - inner_padding * 2, row_offset + cell_scale - inner_padding * 2, fill=color)

def reset_grid(grid):
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

print "Starting Simulation"

root = Tk()
root.title("2031 Simulation")

canvas = Canvas(root, width=(cell_width*cell_scale + padding * 2), height=(cell_height * cell_scale + padding * 2))

grid = np.mat([[0 for x in range(cell_width)] for x in range(cell_height)])
randomize_grid(grid)

draw_grid(grid)

canvas.pack()

atexit.register(root.mainloop)