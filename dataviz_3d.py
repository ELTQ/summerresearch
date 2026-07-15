from networkx.drawing.nx_pydot import graphviz_layout
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *

import os
import networkx as nx
import matplotlib.pyplot as plt

# global variables

TARGET_PATH = "unions/union0.stl"
FIND_NEARBY = 7 # number of nearby points to find
SUCCESS_COLOR = "lightgreen" # points that have been determined "closest" to the target
FAIL_COLOR = "maroon" # points that are not "closest"

def connectToTree(gr, tree): # uses recursion to add objects into our tree. 
    cur_node = tree
    near_child = tree.near
    far_child = tree.far
    if (near_child and near_child.threshold != -1 ):
        if near_child.leaf:
            for leafling in near_child.leaf:
                gr.add_edge(cur_node.sdf.report(), leafling.report())
        else:
            gr.add_edge(cur_node.sdf.report(), near_child.sdf.report())
        
        gr = connectToTree(gr, near_child)

    if (far_child and far_child.threshold != -1 ):
        if far_child.leaf:
            for leafling in far_child.leaf:
                gr.add_edge(cur_node.sdf.report(), leafling.report())
        else:
            gr.add_edge(cur_node.sdf.report(), far_child.sdf.report())
        '''
        print("adding right child at depth", tree.depth())
        print("cur_node =  ", cur_node.threshold)
        print("far_child =  ", far_child.threshold)
        '''
        gr = connectToTree(gr, far_child)
    return gr
    

# Main

if __name__ == "__main__":

    shapes = []
    mesh_path = "unions"
    for mesh in os.listdir(mesh_path):
        if not mesh.endswith('.stl'):
            continue
        shapes.append(sdfs.mesh(os.path.join(mesh_path, mesh)))
        shapes.append(sdfs.invert_mesh(os.path.join(mesh_path, mesh)))




    # shapes.append( sdfs.SDF(sdfs.SDF.circle, 10000000000, 100000000))


    tree = VPTree(shapes)
    tree.split()
    near_branch = tree.near
    far_branch = tree.far
    gr = nx.DiGraph()

    # initialize root node
    gr.add_node(tree.sdf.report())
    gr.add_edge(tree.sdf.report(), near_branch.sdf.report())
    gr.add_edge(tree.sdf.report(), far_branch.sdf.report())
    print(gr)

    target = sdfs.mesh(TARGET_PATH)
    print("target is", target)

    nearest_hits = [0] * FIND_NEARBY
    full_result_knn = tree.searchkcomp(target, FIND_NEARBY)

    print("Ranking of nearest points:")
    for i in range (len(nearest_hits)):
        nearest_hits[i] = full_result_knn[i][1]
        print(i, ": ", full_result_knn[i][0], ", ", full_result_knn[i][1])

    # add all other nodes
    gr = connectToTree(gr, tree)
    print(gr)
    pos = graphviz_layout(gr, prog="twopi")

    ## adapted from
    ## https://stackoverflow.com/questions/27030473/how-to-set-colors-for-nodes-in-networkx
    colors = []

    for node in gr:
        if (node in nearest_hits):
            colors.append(SUCCESS_COLOR)
        else:
            colors.append(FAIL_COLOR) # todo: apply a color gradient for close -> far

    nx.draw_networkx(gr, node_color=colors, pos=pos)
    plt.title("finding complements of unions")
    plt.show()