import scipy
#from mpeg7 import *
import numpy as np
import cv2
import os
from PIL import Image
import scipy.interpolate
import scipy.ndimage
# folder storing mpe7 data
mpeg7_data = '/Users/drew/summerresearch/original'

# folder storing mpeg7 nparray
mpeg7_arrs = "/Users/drew/summerresearch/original_sdfs"

mpeg7_sdfs = "/Users/drew/summerresearch/original_converts"

# turning mpeg7 data into nparray
def mpeg7_to_nparray(image):
    img = Image.open(image)
    img = img.convert('L')
    img = img.resize((256, 256))
    img = np.array(img)
    inside_dist = scipy.ndimage.distance_transform_edt(img)
    outside_dist = scipy.ndimage.distance_transform_edt(cv2.bitwise_not(img))
    sdf = outside_dist - inside_dist
    return sdf

for img in os.listdir(mpeg7_data):
    if not img.endswith('.gif'):
        continue
    sdfs = mpeg7_to_nparray(os.path.join(mpeg7_data, img))
    np.save(os.path.join(mpeg7_arrs, img.split('.')[0] + '.npy'), sdfs)


# turning nparrays into sdf functions
def nparray_to_sdfs(sdf_array):
    shape = sdf_array.shape
    xs = np.arange(256)
    ys = np.arange(256)
    sdf = scipy.interpolate.RegularGridInterpolator((xs, ys), sdf_array)
    return sdf

# loading nparrays as list of sdf objects
def sdf_load(arr_data):
    sdfs = []
    for arr in os.listdir(arr_data):
        filename = os.path.join(mpeg7_arrs, arr)
        if filename[-4:] == ".npy":
            array = np.load(filename, allow_pickle=True)
            sdf = nparray_to_sdfs(array)
            sdf.name = arr.split('.')[0]
            sdfs.append(sdf)
    return sdfs
