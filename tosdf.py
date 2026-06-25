import scipy
from mpeg7 import *
import numpy as np
import cv2
import os

mpeg7_data = 'C:\\Users\\qiuel\\summerresearch\\part1\\mpeg7'

mpeg7_sdfs = "C:\\Users\\qiuel\\summerresearch\\part1\\mpeg7_sdfs"


def mpeg7_to_sdf(image):

    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    inside_dist = scipy.ndimage.distance_transform_edt(img)
    outside_dist = scipy.ndimage.distance_transform_edt(cv2.bitwise_not(img))
    sdf = outside_dist - inside_dist
    return sdf


for img in os.listdir(mpeg7_data):    
    sdfs = mpeg7_to_sdf(img)
    np.save(os.path.join(mpeg7_sdfs, img.split('.')[0] + '.npy'), sdfs)

