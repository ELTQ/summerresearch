from stl import mesh
import numpy as np
import scipy
import cv2 
import meshio
import os 


# Load an STL file (auto-detects binary/ASCII)
# do this for each file in our .off set 
off_mesh = meshio.read("/Users/drew/Downloads/NonRigid/SHREC11_test_database/T42.off")
your_mesh = mesh.Mesh.from_file('T8.stl')

# convert mesh to 0s distances to the surface

'''
inside_dist = scipy.ndimage.distance_transform_edt(data)
outside_dist = scipy.ndimage.distance_transform_edt(cv2.bitwise_not(data))
sdf = outside_dist - inside_dist
'''

# Inspect
print(type(your_mesh.data))

data = your_mesh.data
xs = np.arange(256)
ys = np.arange(256)
sdf = scipy.interpolate.RegularGridInterpolator((xs, ys), data)

print(f'{len(your_mesh)} triangles')
print(f'Bounding box: {your_mesh.min_} to {your_mesh.max_}')

# Save
your_mesh.save('output.stl')