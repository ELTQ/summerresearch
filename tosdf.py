import scipy.ndimage
import numpy as np
import cv2
import os
from PIL import Image

mpeg7_data = 'C:\\Users\\qiuel\\summerresearch\\part1\\mpeg7'

mpeg7_sdfs = "C:\\Users\\qiuel\\summerresearch\\part1\\mpeg7_sdfs"


def mpeg7_to_sdf(image):
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
    sdfs = mpeg7_to_sdf(os.path.join(mpeg7_data, img))
    print(sdfs.shape, img)
    np.save(os.path.join(mpeg7_sdfs, img.split('.')[0] + '.npy'), sdfs)
