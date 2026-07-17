from networkx.drawing.nx_pydot import graphviz_layout
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *

import os
import networkx as nx
import matplotlib.pyplot as plt

# global variables

MESH_PATH = "unions"
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
    k = 3
    getting_input = True
    while getting_input: 
        print(os.listdir(MESH_PATH))
        chosen_stl = input("Which file would you like to find the K compliments of? [e.g. union0.stl]: ")
        if chosen_stl not in os.listdir(MESH_PATH):
            print("Invalid choice, try again")
            continue
        comp_near_choice = input("Would you like to find the K nearest neighbors of K nearest compliments [neighbors / compliments]: ")
        if comp_near_choice == "neighbors" or comp_near_choice == "Neighbors":
            k = input("How many neighbors would you like to find: ")
            if str.isnumeric(k):
                k = int(k)
                getting_input = False
            else:
                print("Invalid input, try again")
                continue
        elif comp_near_choice == "compliments" or comp_near_choice == "Compliments":
            k = input("How many compliments would you like to find: ")
            if str.isnumeric(k):
                k = int(k)
                getting_input = False
            else:
                print("Invalid input, try again")
                continue
        else: 
            print("Invalid input, try again")
            continue

    shapes = []
    for mesh in os.listdir(MESH_PATH):
        if not mesh.endswith('.stl'):
            continue
        shapes.append(sdfs.mesh(os.path.join(MESH_PATH, mesh)))
        shapes.append(sdfs.invert_mesh(os.path.join(MESH_PATH, mesh)))

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

    target = sdfs.mesh(chosen_stl)
    print("target is", target)

    nearest_hits = [0] * k
    if (comp_near_choice == "compliments" or comp_near_choice == "Compliments" ):
        full_result_knn = tree.searchkcomp(target, k)
    elif (comp_near_choice == "neighbors" or comp_near_choice == "Neighbors"):
        full_result_knn = tree.searchKNN(target, k)

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
    plt.title("finding", comp_near_choice, "of unions")
    plt.show()