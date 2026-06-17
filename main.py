from sdflib.sdfs import * 
import random
import vpt.tree as tree

circ1 = SDF(func=SDF.circle, ID=1)
circ2 = SDF(func=SDF.circle, ID=2)

pointx = []
pointy = []
points = []
for i in range(5):
    points.append((random.randint(-5, 5), random.randint(-5, 5)))
print("the difference between circles is", circ1.compare(circ2, points))