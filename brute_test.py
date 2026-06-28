from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *
from vpt.heap import *
import random 

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

    # using the k-nearest neighbors method
    full_result_knn = tree.searchkNN(target, FIND_NEARBY)
    nearest_hits = [0] * FIND_NEARBY
    for i in range (len(nearest_hits)):
        nearest_hits[i] = full_result_knn[i][1].report()

    # using the brute force method
    brute_max = []
    heapq.heapify_max(brute_max) # is this necessary on an empty list? 
    for my_shape in shapes:
        if len(brute_max) < FIND_NEARBY: # if we haven't found enough nearby yet
            tuple_i = ( mse(points, my_shape, target), my_shape )
            heapq.heappush_max(brute_max, tuple_i)
        else: # if there are enough nodes in our max heap
            root = heapq.heappop_max(brute_max)
            if (root[0] > mse(points, my_shape, target)): # if the furthest distance of our chosen points is greater than the shape we've found,
                heapq.heappush_max(brute_max, (mse(points, my_shape, target), my_shape)) # add it to the heap
            else:
                heapq.heappush_max(brute_max, root) # otherwise, put the root back on top

    brute_hits = [0] * FIND_NEARBY
    for i in range (len(brute_hits)):
        brute_hits[i] = heapq.heappop_max(brute_max)[1].report()


    # code derived from 
    # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
    if len(set(brute_hits) & set(nearest_hits)) == FIND_NEARBY: # comparing the actual descriptions, as the references to the SDFs may have changed at this point
        #print("good job!")
        count += 1
    else:
        print(set(nearest_hits).difference(set(brute_hits)), "was only in the KNN method")
        print(set(brute_hits).difference(set(nearest_hits)), "was only in the Brute method")
        pass



if count == RUNS:
    print("all tests passed!")
else:
    print("some tests failed.... count = ", count)
