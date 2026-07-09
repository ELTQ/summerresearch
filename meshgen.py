import trimesh
import numpy as np
import os

box = trimesh.creation.box(extents=[1,1,1])
folder ="C:\\Users\\qiuel\\summerresearch\\part1\\meshes"

for i in range(0, 90, 10):
    radian = np.radians(i)
    x_axis = [1, 0, 0]
    matrix = trimesh.transformations.rotation_matrix(radian, x_axis)
    mesh = box.copy()
    mesh = mesh.apply_transform(matrix)
    mesh.export(os.path.join(folder, str(i) + ".stl"))
