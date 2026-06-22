from networkx.drawing.nx_pydot import graphviz_layout
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *

import networkx as nx
import random 
import matplotlib.pyplot as plt

def connectToTree(gr, tree):
    cur_node = tree
    near_child = tree.left
    far_child = tree.right
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

circs = generate_circles(100)
print(len(circs))


tree = VPTree(points, circs)
tree.split()
near_branch = tree.left
far_branch = tree.right
gr = nx.DiGraph()

# initialize root node
gr.add_node(tree.sdf.report())
gr.add_edge(tree.sdf.report(), near_branch.sdf.report())
gr.add_edge(tree.sdf.report(), far_branch.sdf.report())
print(gr)

# add all other nodes
gr = connectToTree(gr, tree)
print(gr)
pos = graphviz_layout(gr, prog="twopi")
nx.draw_networkx(gr, pos)
plt.show()