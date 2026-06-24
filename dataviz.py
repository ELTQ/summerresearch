from networkx.drawing.nx_pydot import graphviz_layout
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *

import networkx as nx
import random 
import matplotlib.pyplot as plt

def connectToTree(gr, tree):
    cur_node = tree
    near_child = tree.near
    far_child = tree.far
    if (near_child and near_child.threshold != -1 ):
        
        gr.add_edge(cur_node.sdf.report(), near_child.sdf.report())
        '''
        print("adding left child at depth", tree.depth())
        print("cur_node =  ", cur_node.threshold)
        print("near_child =  ", near_child.threshold)
'''
        gr = connectToTree(gr, near_child)
    if (far_child and far_child.threshold != -1 ):
        
        gr.add_edge(cur_node.sdf.report(), far_child.sdf.report())
        '''
        print("adding right child at depth", tree.depth())
        print("cur_node =  ", cur_node.threshold)
        print("far_child =  ", far_child.threshold)
        '''
        gr = connectToTree(gr, far_child)
    return gr
    

# Main
pointx = []
pointy = []
points = [(random.randint(-300, 300), random.randint(-300, 300)) for i in range(20)]

shapes = generate_circles(50)
tris = generate_triangles(50)

shapes.append( sdfs.SDF(sdfs.SDF.circle, 10000000000, 100000000))

shapes += (tris)

tree = VPTree(points, shapes)
tree.split()
near_branch = tree.near
far_branch = tree.far
gr = nx.DiGraph()

# initialize root node
gr.add_node(tree.sdf.report())
gr.add_edge(tree.sdf.report(), near_branch.sdf.report())
gr.add_edge(tree.sdf.report(), far_branch.sdf.report())
print(gr)

target = generate_circles(1)
nearest_target = tree.searchkNN(target[0], 5)


print(target[0])
for i in nearest_target:
    print(i[1])

# add all other nodes
gr = connectToTree(gr, tree)
print(gr)
pos = graphviz_layout(gr, prog="twopi")
nx.draw_networkx(gr, pos)
plt.show()