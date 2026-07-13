
import numpy as np
import os
import trimesh
import random

# generate trimesh spheres with radius r at x, y, z position
def generate_sphere(r, x, y, z):
    sphere = trimesh.creation.icosphere(radius=r)
    sphere.apply_translation([x,y,z])
    return sphere

# generate return a list of n spheres within range 0 to 1 with radius between 0 to 1
def rand_sphere_union(n):
    spheres = []
    for i in range(n):
        xi = random.uniform(0,1)
        yi = random.uniform(0,1)
        zi = random.uniform(0,1)
        ri = random.uniform(0,1)
        spheres.append(generate_sphere(ri, xi, yi, zi))
    return spheres


union_dir = "C:\\Users\\qiuel\\summerresearch\\part1\\unions"

# generate 10 union shape each made with 10 spheres
for i in range(10):
    spheres = rand_sphere_union(10)
    un = trimesh.boolean.union(spheres)
    un.export(os.path.join(union_dir, "union" + str(i) + ".stl"))
