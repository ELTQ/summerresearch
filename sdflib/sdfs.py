# import statements
import scipy.ndimage
import numpy as np
import cv2
import os
from PIL import Image
import scipy.interpolate
import scipy.ndimage
import math
import trimesh as tri

# main class definition
class SDF:
    def __init__(self): 
        self.name = "null"
        self.midpoint = (0, 0)
    def __str__(self):
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))
    def report(self):
        return (self.name)


# inheritance
class circle(SDF):
    '''
    Constructor for a two-dimensional circle.
    Takes in the circle's center point as two parameters.
    The default name will be "circle".
    '''
    def __init__(self, cx, cy):
        self.name = "circle"
        self.midpoint = (cx, cy)

    '''
    Gets the unsigned distance between the circle's edge and a given point. 
    r = radius of the circle
    '''
    def __call__(self, target_point, r = 1.0):
        cx = self.midpoint[0]
        cy = self.midpoint[1]
        distance = math.dist((cx, cy), (target_point[0], target_point[1])) - r
        return distance

    '''
    Returns a string describing a circle's name and midpoint. Useful for classification of various circles and displaying them in matplotlib.
    '''
    def report(self):
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))


class triangle(SDF):
    '''
    Constructor for a two-dimensional circle.
    Takes in the circle's center point as two parameters.
    The default name will be "circle".
    '''
    def __init__(self, cx, cy):
        self.name = "triangle"
        self.midpoint = (cx, cy)

    '''
    Gets the signed distance to an equilateral triangle's edge from a given target point. 
    r = size of the triangle (?)
        Adapted from:
        https://iquilezles.org/articles/distfunctions2d/
    '''
    def __call__(self, target_point, r = 1.0):
        cx = self.midpoint[0]
        cy = self.midpoint[1]
        x = target_point[0]
        y = target_point[1]
        k = math.sqrt(3.0) # number of sides?
        x = abs(x) - r
        y = abs(y) + r/k
        if (((x + k) * y) > 0):
            x = ((x-k)*y) / 2
            y = ((-k*x)-y) / 2
        x -= np.clip(x, -2*r, 0)
        return -math.dist((cx, cy), (x, y)) * math.copysign(1, y) # we dont have a sign function so this is what i need to do instead

    '''
    Returns a string describing the triangle.
    '''
    def report(self):
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))


'''
The 'image' class inherits from the SDF class, and interprets a given 256*256 .gif image with two colors as a Signed Distance Function.
Uses the scipy.ndimage package to create a signed distance field, and is smoothed with the scipy.interpolate.RegularGridInterpolator method.
'''
class image(SDF):
    '''
    Constructor for a 2D image SDF. The value of a point with regards to this shape will be negative when inside the shape, 0 when on the border, 
    and positive when outside the shape. 
    dir = filepath where the 2D .gif image is located.
    '''
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
    

    '''
    Uses the Regular Grid Interpolator object to interpret the list of given points.
    pts = a list of points in 2D as tuple objects.
    '''
    def __call__(self, pts):
        return self.sdf(pts)
    
    '''
    If printed to the console, the image SDF will return the name of its file.
    '''
    def __str__(self):
        return (self.name)


'''
The 'mesh' class inherits from the SDF superclass, and is used to interpret 3D SDFs from the .stl file format using trimesh.
Considered to be a "ligand", or a "key". 
'''
class mesh(SDF): # negative inside mesh, positive outside mesh
    '''
    Constructor for a 3D mesh SDF. The value of a point with regards to this shape will be negative when inside the shape, 0 when on the border, 
    and positive when outside the shape. 
    dir = filepath where the 3D .stl mesh is located.
    '''
    def __init__(self, dir):
        self.name = os.path.basename(dir).split('.')[0]
        self.midpoint = (0, 0)
        mesh = tri.load_mesh(dir)
        mesh.apply_translation(-mesh.bounds[0])
        scale = 1 / mesh.extents.max()
        mesh.apply_scale(scale)
        self.mesh = mesh
    
    '''
    Returns a list of distances to a given list of points.
    Using trimesh's library causes this to take a while at times.
    
    There is a negative sign here, unlike the __call__ method in the invert_mesh class.
    '''
    def __call__(self, pts):
        return -tri.proximity.signed_distance(self.mesh, pts)


'''
If the mesh class is a "key", then the invert_mesh class is a "pocket", "keyhole", "binding site", or "receptor". 
Could theoretically be used in reverse, but for consistency, we recommend using the mesh class for 3D "key" objects, and the invert_mesh class for "receptors".
'''
class invert_mesh(SDF): # positive inside mesh, negative outside mesh
    '''
    The value of a point with regards to this shape will be POSITIVE when inside the shape, 0 when on the border, 
    and NEGATIVE when outside the shape. This is the "inverse" of a normal mesh object.
    '''
    def __init__(self, dir):
        self.name = str("Inverted " + os.path.basename(dir).split('.')[0])
        self.midpoint = (0, 0)
        mesh = tri.load_mesh(dir)
        mesh.apply_translation(-mesh.bounds[0])
        scale = 1 / mesh.extents.max()
        mesh.apply_scale(scale)
        self.mesh = mesh
    
    def __call__(self, pts):
        '''
        No negative sign here, unlike the __call__ method in the mesh class.
        '''
        return tri.proximity.signed_distance(self.mesh, pts) 


'''
Depreciated function to compare two SDFs. Do not use.
'''
def compare_shapes(self, other, points):
    # compare two SDFs 
    total = 0
    for x, y in points:
        total += (self(self, x, y) - other(other, x, y)) ** 2
    return (total / len(points))