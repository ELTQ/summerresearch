from networkx.drawing.nx_pydot import graphviz_layout
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *
from vpt.heap import *

import networkx as nx
import random 
import matplotlib.pyplot as plt

FIND_NEARBY = 10
RUNS = 100
count = 0

for loop in range(RUNS):
    # Main

    pointx = []
    pointy = []
    points = [(random.randint(-300, 300), random.randint(-300, 300)) for i in range(20)]

    shapes = generate_circles(50)
    tris = generate_triangles(50)

    shapes += (tris)

    tree = VPTree(points, shapes)
    tree.split()


    target = generate_circles(1)[0]
    #print("target is", target)

    nearest_hits = [0] * FIND_NEARBY
    full_result_knn = tree.searchkNN(target, FIND_NEARBY)

    #print("Ranking of nearest points:")
    for i in range (len(nearest_hits)):
        nearest_hits[i] = full_result_knn[i][1].report()
        #print(i, ": ", full_result_knn[i][0], ", ", full_result_knn[i][1])

    brute_max = []
    heapq.heapify_max(brute_max)

    for i in range(FIND_NEARBY):
        heapq.heappush_max(brute_max, ( mse(points, shapes[i], target), shapes[i]) )

    for my_shape in shapes[FIND_NEARBY:]: # skip the first few, as they've already been added
        root = heapq.heappop_max(brute_max)
        if (root[0] > mse(points, my_shape, target)):
            heapq.heappush_max( brute_max, (mse(points, my_shape, target), my_shape))
        else:
            heapq.heappush_max(brute_max, root)



    #print("Ranking of nearest points (brute force): ")
    brute_hits = [0] * FIND_NEARBY
    for i in range (len(brute_hits)):
        brute_hits[i] = heapq.heappop_max(brute_max)[1].report()
        #print(i, ": ", brute_hits[i])


    # code derived from 
    # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
    if len(set(brute_hits) & set(nearest_hits)) == FIND_NEARBY:
        #print("good job!")
        count += 1
        

if count == RUNS:
    print("all tests passed!")
else:
    print("some tests failed.... count = ", count)
