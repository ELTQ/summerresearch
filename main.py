import os
import numpy as np
from sdflib.sdfs import * 
import random
import vpt.tree as tree
from vpt.tree import VPTree, mse

from tosdf import *

mpeg7_arrs = "C:\\Users\\qiuel\\summerresearch\\part1\\mpeg7_arrs"
shapes = sdf_load(mpeg7_arrs)
pointx = []
pointy = []
points = []

for i in range(100):
    points.append((random.randint(0, 255), random.randint(0, 255)))

apple1 = shapes[0]
tree = VPTree(points, shapes[1:])
tree.split()

print("the nearest neighbor of circf is", tree.searchkNN(apple1, 10))
