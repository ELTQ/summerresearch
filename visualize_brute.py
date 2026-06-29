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

    # using the brute force method
    brute_max = []
    for my_shape in shapes:
        if len(brute_max) < FIND_NEARBY: # if we haven't found enough nearby yet
            tuple_i = ( mse(points, my_shape, target), my_shape )
            heapq.heappush_max(brute_max, tuple_i)
        else: # if there are enough nodes in our max heap
            heapq.heapify_max(brute_max)
            root = heapq.heappop_max(brute_max)
            if (root[0] > mse(points, my_shape, target)): # if the furthest distance of our chosen points is greater than the shape we've found,
                heapq.heappush_max(brute_max, (mse(points, my_shape, target), my_shape)) # add it to the heap
            else:
                heapq.heappush_max(brute_max, root) # otherwise, put the root back on top

    brute_hits = [0] * FIND_NEARBY
    brute_sdfs = [item[1] for item in brute_max]

    for circle in shapes:
        plot_sdf_circle(circle, 'r')
    for circle in brute_sdfs:
        plot_sdf_circle(circle, 'b')
    brute_copy = copy.deepcopy(brute_max)
    for i in range (len(brute_hits)):
        heapq.heapify_max(brute_copy)
        brute_hits[i] = heapq.heappop_max(brute_copy)[1].report()

    # draw circle of furthest radius 
    radius = heapq.heappop_max(brute_max)[1]
    int_radius = math.dist( radius.midpoint, target.midpoint)
    print("furthest is ", int_radius, "units away")
    axes.add_line(lines.Line2D((target.midpoint[0], radius.midpoint[0] ), (target.midpoint[1], radius.midpoint[1])))

    axes.add_artist(plt.Circle(target.midpoint, int_radius, fill = False, color='r')) # radius of 7, filled in


plt.axes = axes
plt.grid(True, 'both', 'both')
plt.title("Finding Nearest Neighors using Brute Force")
plt.show()