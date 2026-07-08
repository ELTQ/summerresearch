import os
import numpy as np
from sdflib import sdfs
import random
import vpt.tree as tree
from vpt.tree import VPTree, rmse
import cv2
from PIL import Image, ImageOps
import matplotlib.pyplot as plt





shrec = "C:\\Users\\qiuel\\summerresearch\\part1\\shrec11_stl"

shrec_samp = ("C:\\Users\\qiuel\\summerresearch\\part1\\shrec11_stl\\T0.stl")


shapes = []
for img in os.listdir(shrec):
    if not img.endswith('.stl'):
        continue
    shapes.append(sdfs.mesh(os.path.join(shrec, img)))


for shape in shapes:
    if shape.name == "T0.stl":
        t0 = shape
        break

tree = VPTree(shapes[:])
tree.split()
print("target is " + t0.name)

others = sorted(tree.searchkcomp(t0, 4))

print("the k nearest complements are", others)


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
