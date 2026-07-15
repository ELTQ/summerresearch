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
mpeg7_imgs = "keys_and_pockets"

mimg = Image.open("keys_and_pockets/mickey_key_inverted.gif")

"""
for frame in range(-90, 90, 10):
    mimg = mimg.rotate(10, expand=False)
    mimg.save("C:\\Users\\qiuel\\summerresearch\\part1\\keys_and_pockets\\mickey_key_" + str(frame) + ".gif")
"""


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

for shape in shapes:
    if shape.name == "mickey_key_inverted":
        mickey_pocket = shape
        break
tree = VPTree(shapes[:])
tree.split()

print("target is " + mickey_pocket.name)
others = sorted(tree.searchkcomp(mickey_pocket, 4))
print(others)
#quit()

# find the nearest complement to mickey_pocket
print("the nearest complement is", sorted(others))

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
# changing pixel values to 0 or 255 for visualization
"""

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