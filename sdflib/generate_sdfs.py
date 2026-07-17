from . import sdfs
import random

# constants
MIN_COORD = 0
MAX_COORD = 500
RADIUS_RANGE = 7 


'''
Generate a list of random circle SDFs to stress test our tree code. 
Parameters: 
    count: the number of requested circle SDFs
Returns:
    a list of circles at random positions
'''

def generate_circles(count):
    circles = [0] * count
    for i in range(count): 
        x_coord = random.randint(MIN_COORD, MAX_COORD) # midpoint of circle
        y_coord = random.randint(MIN_COORD, MAX_COORD)

        circles[i] = sdfs.circle(x_coord, y_coord)
    return circles

'''
Generate a list of random equilateral SDFs to stress test our tree code. 
Parameters: 
    count: the number of requested triangle SDFs
Returns:
    a list of triangles at random positions
'''

def generate_triangles(count):

    triangles = [0] * count
    for i in range(count): 
        x_coord = random.randint(MIN_COORD, MAX_COORD) # midpoint of triangle
        y_coord = random.randint(MIN_COORD, MAX_COORD)
        triangles[i] = sdfs.triangle(x_coord, y_coord)
    return triangles

        