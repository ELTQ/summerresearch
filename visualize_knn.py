import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np
import copy
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *


# code adapted from https://www.geeksforgeeks.org/python/how-to-draw-a-circle-using-matplotlib-in-python/
figure, axes = plt.subplots()

axes.set_xlim((-300, 300))
axes.set_ylim((-300, 300))
axes.set_aspect(1)

FIND_NEARBY = 10
RUNS = 1
POINTS_NUM = 100
count = 0
right = 0
wrong = 0
first_pos_error_knn = 0
first_pos_error_brute = 0

def plot_sdf_circle(plotted_circle, char_color):
    axes.add_artist(plt.Circle(plotted_circle.midpoint, 7, fill = True, color=char_color)) # radius of 7, filled in

for loop in range(RUNS):
    # Main

    pointx = []
    pointy = []
    points = [(random.randint(-300, 300), random.randint(-300, 300)) for i in range(POINTS_NUM)]

    shapes = generate_circles(100)
    tris = generate_triangles(0)

    shapes += (tris)

    tree = VPTree(points, shapes)
    tree.split()

    target = generate_circles(1)[0]

    plot_sdf_circle(target, 'g')

    # using the k-nearest neighbors method
    full_result_knn = tree.searchkNN(target, FIND_NEARBY)
    nearest_hits = [0] * FIND_NEARBY
    for i in range (len(nearest_hits)):
        nearest_hits[i] = full_result_knn[i][2] # stored at 2 now

    for circle in shapes:
        plot_sdf_circle(circle, 'r')
    for circle in nearest_hits:
        plot_sdf_circle(circle, 'b')

    # draw circle of furthest radius 
    # need to find furthest (least similar):
    max = -1
    furthest_sdf = nearest_hits[0]

    for sdf in (nearest_hits):
        if (mse(points, target, sdf) > max):
            max = mse(points, target, sdf)
            furthest_sdf = sdf
    
    radius = furthest_sdf
    int_radius = math.dist( radius.midpoint, target.midpoint)
    
    axes.add_line(lines.Line2D((target.midpoint[0], radius.midpoint[0] ), (target.midpoint[1], radius.midpoint[1])))
    print("furthest is ", int_radius, "units away")

    axes.add_artist(plt.Circle(target.midpoint, int_radius, fill = False, color='r')) # radius of 7, filled in


    # code derived from 
    # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
    
plt.axes = axes
plt.grid(True, 'both', 'both')
plt.title("Finding Nearest Neighors using KNN Search")
plt.show()