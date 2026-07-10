# SDF objects class
import scipy.ndimage
import numpy as np
import cv2
import os
from PIL import Image
import scipy.interpolate
import scipy.ndimage
import math
import trimesh as tri

class SDF:
    def __init__(self): 
        self.name = "null"
        self.midpoint = (0, 0)
    def __str__(self):
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))


class circle(SDF):
    def __init__(self, cx, cy):
        self.name = "circle"
        self.midpoint = (cx, cy)

    def __call__(self, target_point, r = 1.0):
        cx = self.midpoint[0]
        cy = self.midpoint[1]
        distance = math.dist((cx, cy), (target_point[0], target_point[1])) - r
        return distance

    def report(self):
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))


class triangle(SDF):
    def __init__(self, cx, cy):
        self.name = "triangle"
        self.midpoint = (cx, cy)

    def __call__(self, x, y, r = 1.0):
        cx = self.midpoint[0]
        cy = self.midpoint[1]

        k = math.sqrt(3.0) # number of sides?
        x = abs(x) - r
        y = abs(y) + r/k
        if (((x + k) * y) > 0):
            x = ((x-k)*y) / 2
            y = ((-k*x)-y) / 2
        x -= np.clip(x, -2*r, 0)
        return -math.dist((cx, cy), (x, y)) * math.copysign(1, y) # we dont have a sign function so this is what i need to do instead

    def report(self):
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))

class image(SDF):
    def __init__(self, dir):
        self.name = os.path.basename(dir).split('.')[0]
        img = Image.open(dir)
        img = img.convert('L')
        img = img.resize((256, 256))
        img = np.array(img)
        inside_dist = scipy.ndimage.distance_transform_edt(img)
        outside_dist = scipy.ndimage.distance_transform_edt(cv2.bitwise_not(img))
        sdf_arr = outside_dist - inside_dist
        shape = sdf_arr.shape
        xs = np.arange(shape[0])
        ys = np.arange(shape[1])
        self.sdf = scipy.interpolate.RegularGridInterpolator((xs, ys), sdf_arr)
    

    def __call__(self, pts):
        return self.sdf(pts)
    
    def __str__(self):
        return (self.name)

class mesh(SDF):
    def __init__(self, dir):
        self.name = os.path.basename(dir).split('.')[0]
        mesh = tri.load_mesh(dir)
        self.mesh = mesh
    
    def __call__(self, pts):

        return tri.proximity.signed_distance(self.mesh, pts) # returns the distance to a (x, y, z) point. 

    def __str__(self):
        return (self.name)


def compare_shapes(self, other, points):
    # compare two SDFs 
    total = 0
    for x, y in points:
        total += (self(self, x, y) - other(other, x, y)) ** 2
    return (total / len(points))