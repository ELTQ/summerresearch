from networkx.drawing.nx_pydot import graphviz_layout
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *

import networkx as nx
import random 
import matplotlib.pyplot as plt

def connectToTree(gr, tree):
    cur_node = tree
    left_child = tree.left
    right_child = tree.right
    if (left_child):
        gr.add_node(left_child.threshold)
        gr.add_edge(cur_node.threshold, left_child.threshold)
        print("adding left child at depth", tree.depth())
        gr = connectToTree(gr, left_child)
    if (right_child):
        print("adding right child at depth", tree.depth())
        gr.add_node(right_child.threshold)
        gr.add_edge(cur_node.threshold, right_child.threshold)
        gr = connectToTree(gr, right_child)
    return gr
    

# Main
pointx = []
pointy = []
points = [(random.randint(-300, 300), random.randint(-300, 300)) for i in range(20)]

circs = generate_circles(100)

ucirc = SDF(func=SDF.circle, cx=0, cy=0)

tree = VPTree(points, circs)
tree.split()
left_branch = tree.left
right_branch = tree.right 

gr = nx.DiGraph()
print(tree.depth())

tree_depth = tree.depth()

gr.add_node(tree.threshold)
gr = connectToTree(gr, tree)

print(gr)
pos = graphviz_layout(gr, prog="dot")
nx.draw_networkx(gr)

plt.show()