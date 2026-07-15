import os
import numpy as np
from sdflib import sdfs
import random
import vpt.tree as tree
from vpt.tree import VPTree, rmse
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import rtree


if __name__ == "__main__":

    points = [(random.randint(-300, 300), random.randint(-300, 300)) for i in range(20)]
    shrec = "shrec11_stl"
    shrec_samp = "shrec11_stl/T0.stl"

    cube_meshes = "unions"
    cube_standard = "unions/union0.stl"

    print(os.listdir(cube_meshes))
    chosen_stl_path = input("Which .stl would you like to compare? [e.g. '0.stl']: ")
    chosen_count = input("How many complimentary .stl files would you like to find?: ")

    shapes = []

    for img in os.listdir(cube_meshes):
        if not img.endswith('.stl'):
            continue
        shapes.append(sdfs.mesh(os.path.join(cube_meshes, img)))

    neutral_point = sdfs.mesh(os.path.join(cube_meshes, chosen_stl_path))
    tree = VPTree(points, shapes)
    tree.split()
    print("target is " + neutral_point.name)
    others = sorted(tree.searchkNN(neutral_point, int(chosen_count)))
    print("the k nearest neighbors are", others)

    """
    DEN = 32

    xv, yv = np.meshgrid(np.linspace(0,1,DEN),np.linspace(0,1,DEN))
    coords = np.stack([np.reshape(xv,-1), np.reshape(yv,-1)],1)


    fig,ax = plt.subplots(1,len(others)+1)

    evaluated = mickey_pocket(coords)
    ax[0].matshow(evaluated.reshape(DEN,DEN).T)

    for i in range(len(others)):
        evaluated = others[i][2](coords)
        ax[i+1].matshow(evaluated.reshape(DEN,DEN).T)

    plt.show()
    """
