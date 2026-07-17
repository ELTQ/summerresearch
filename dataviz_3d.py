# import statements
from networkx.drawing.nx_pydot import graphviz_layout
from sdflib.generate_sdfs import *
from sdflib.sdfs import *
from vpt.tree import *

import os
import networkx as nx
import matplotlib.pyplot as plt

# global variables
MESH_PATH = "unions" # directory where the meshes are to be compared to one another. slow if used on complex .stl files
TARGET_PATH = "unions/union0.stl" # default target mesh, unused
FIND_NEARBY = 7 # number of nearby points to find
SUCCESS_COLOR = "lightgreen" # points that have been determined "closest" to the target
FAIL_COLOR = "maroon" # points that are not "closest"
MATCH_COLOR = "gold" # points that are identical to the target

def connectToTree(gr, tree): # uses recursion to add objects into our tree. used for both 2D and 3D. 
    cur_node = tree
    near_child = tree.near
    far_child = tree.far

    # if there is a near child, and the near child has been initialized, add things in this child branch.
    if (near_child and near_child.threshold != -1 ):
        if near_child.leaf: # if the child is a leaf node, add its leaves into our tree
            for leafling in near_child.leaf:
                gr.add_edge(cur_node.sdf.report(), leafling.report()) # uses the report functions as descriptors to create nodes 
        else: # otherwise, add its single sdf into our tree
            gr.add_edge(cur_node.sdf.report(), near_child.sdf.report())
        
        # recursively add this tree's information
        gr = connectToTree(gr, near_child)

    # if there is a far child, and the far child has been initialized, add things in this child branch.
    if (far_child and far_child.threshold != -1 ):
        if far_child.leaf:
            for leafling in far_child.leaf:
                gr.add_edge(cur_node.sdf.report(), leafling.report())
        else:
            gr.add_edge(cur_node.sdf.report(), far_child.sdf.report())

        # recursively add this tree's information
        gr = connectToTree(gr, far_child)
    return gr
    

# Main
if __name__ == "__main__":
    k = 3 # default value for nearest neighbors, used if all else fails

    # input validation
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
            k = input("How many compliments would you like to find (including chosen .stl): ")
            if str.isnumeric(k):
                k = int(k)
                getting_input = False
            else:
                print("Invalid input, try again")
                continue
        else: 
            print("Invalid input, try again")
            continue
    # end input validation
        
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


    target = sdfs.mesh(os.path.join(MESH_PATH, chosen_stl)) # gets full path to file
    print("target is", target)


    nearest_hits = [0] * k # initializes a list of the k nearest points to our target
    if (comp_near_choice == "compliments" or comp_near_choice == "Compliments" ):
        full_result_knn = tree.searchkcomp(target, k)
    elif (comp_near_choice == "neighbors" or comp_near_choice == "Neighbors"):
        full_result_knn = tree.searchkNN(target, k)

    
    self = target
    print("Ranking of nearest points:")
    for i in range (len(nearest_hits)):
        nearest_hits[i] = full_result_knn[i][1] # gets the node object from full results 
        if (full_result_knn[i][0] == 0.0):
            self = full_result_knn[i][1]
        print(i, ": ", full_result_knn[i][0], ", ", full_result_knn[i][1])


    # initialize root node
    gr.add_node(tree.sdf.report())
    gr.add_edge(tree.sdf.report(), near_branch.sdf.report())
    gr.add_edge(tree.sdf.report(), far_branch.sdf.report())
    # add all other nodes
    gr = connectToTree(gr, tree)
    print(gr)
    pos = graphviz_layout(gr, prog="twopi")

    ## adapted from
    ## https://stackoverflow.com/questions/27030473/how-to-set-colors-for-nodes-in-networkx
    colors = []

    for node in gr:
        if (node == self):
            colors.append(MATCH_COLOR)
        elif (node in nearest_hits):
            colors.append(SUCCESS_COLOR)
        else:
            colors.append(FAIL_COLOR) # todo: apply a color gradient for close -> far

    nx.draw_networkx(gr, pos=pos, node_color=colors)

    title_string = "Finding " + str(k) + " " + comp_near_choice + " of .stl meshes in the path /" + MESH_PATH + " compared to " + chosen_stl
    plt.title(title_string)
    plt.show()