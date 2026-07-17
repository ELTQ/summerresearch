
import numpy as np
import os
import trimesh
import random

# generate spheres with vdw radiis at x, y, z position
def generate_sphere(x, y, z):
    vdw_radii = {"H": 1.1, "C": 1.7, "N":1.55, "O":1.52, "S":1.8, "P": 1.8}
    radii = random.choice(list(vdw_radii.values()))
    sphere = trimesh.creation.icosphere(radius=radii)
    sphere.apply_translation([x,y,z])
    return sphere

# generate return a list of n spheres within range 0 to 1 with random vdw radii
def rand_sphere_union(n):
    spheres = []
    for i in range(n):
        xi = random.uniform(0,1)
        yi = random.uniform(0,1)
        zi = random.uniform(0,1)
        spheres.append(generate_sphere(xi, yi, zi))
    return spheres


union_dir = "C:\\Users\\qiuel\\summerresearch\\part1\\unions"

# generate 20 union shapes each made with 20 spheres
for i in range(20):
    spheres = rand_sphere_union(10)
    un = trimesh.boolean.union(spheres)
    un.export(os.path.join(union_dir, "union" + str(i) + ".stl"))
