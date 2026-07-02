import os
import numpy as np
from sdflib import sdfs
import random
import vpt.tree as tree
from vpt.tree import VPTree, rmse
import cv2
from PIL import Image, ImageOps
import matplotlib.pyplot as plt


'''


'''
mpeg7_imgs = "C:\\Users\\qiuel\\summerresearch\\part1\\keys_and_pockets"

mimg = Image.open("C:\\Users\\qiuel\\summerresearch\\part1\\keys_and_pockets\\mickey_pocket.gif")

shapes = []
for img in os.listdir(mpeg7_imgs):
    if not img.endswith('.gif'):
        continue
    shapes.append(sdfs.image(os.path.join(mpeg7_imgs, img)))


pointx = []
pointy = []
points = []

for i in range(1000):
    points.append((random.randint(0, 255), random.randint(0, 255)))

print(len(shapes))

mickey_key = shapes[0]

tree = VPTree(points, shapes[1:])
tree.split()
print("target is " + mickey_key.name)

print("the nearest complement of circf is", tree.searchkcomp(mickey_key, 7))

"""
print(mickey_pocket.name)
print(mickey_key(128,128), mickey_pocket(128,128))
print(mickey_key.sdf_arr, -mickey_pocket.sdf_arr)
#print("the nearest complement of circf is", tree.searchkNN(mickey_key, 1))

mickey_key_array = mickey_key.sdf_arr  
mickey_pocket_array = mickey_pocket.sdf_arr

for i in range(256):
    for j in range(256):
        if mickey_key_array[i][j] < 0:
            mickey_key_array[i][j] = 0
        else:
            mickey_key_array[i][j] = 255

for i in range(256):
    for j in range(256):
        if mickey_pocket_array[i][j] < 0:
            mickey_pocket_array[i][j] = 0
        else:
            mickey_pocket_array[i][j] = 255

# Visualize the pixels
plt.imshow(mickey_key_array, cmap='gray', interpolation='nearest')
plt.colorbar() # Adds a bar showing intensity scale
plt.show()

plt.imshow(mickey_pocket_array, cmap='gray', interpolation='nearest')
plt.colorbar() # Adds a bar showing intensity scale
plt.show()
"""
