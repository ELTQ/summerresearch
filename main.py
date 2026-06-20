from sdflib.sdfs import * 
from sdflib.generate_sdfs import *
import random
import vpt.tree as tree
from vpt.tree import VPTree, mse


pointx = []
pointy = []
points = [(random.randint(-300, 300), random.randint(-300, 300)) for i in range(20)]

circs = generate_circles(100)

ucirc = SDF(func=SDF.circle, cx=0, cy=0)

tree = VPTree(points, circs, ucirc)
tree.split()
left_branch = tree.left
right_branch = tree.right 

tree.report()
tree.left.report()
tree.right.report()
if left_branch.left:
    left_branch.left.report()
if left_branch.right:
    left_branch.right.report()   
if right_branch.left:
    right_branch.left.report()
if right_branch.right:
    right_branch.right.report()