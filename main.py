from sdflib.sdfs import * 
import random
import vpt.tree as tree
from vpt.tree import VPTree, mse

circ1 = SDF(func=SDF.circle, ID=1)
circ2 = SDF(func=SDF.circle, ID=2)
circ3 = SDF(func=SDF.circle, ID=3)
circ4 = SDF(func=SDF.circle, ID=4)
circ5 = SDF(func=SDF.circle, ID=5)
circ6 = SDF(func=SDF.circle, ID=6)

pointx = []
pointy = []
points = []
for i in range(5):
    points.append((random.randint(-5, 5), random.randint(-5, 5)))
print("the difference between circles is", circ1.compare(circ2, points))


circs = [circ1, circ2, circ3, circ4, circ5, circ6]

ucirc = SDF(func=SDF.circle, ID=1)

tree = VPTree(points, circs, ucirc)
tree.split()
left = tree.left.sdfs
right = tree.right.sdfs
for i in range (len(left)):
    print("left circle: ", left[i].ID, "with distance")
print(tree.left.sdfs, tree.right.sdfs)
