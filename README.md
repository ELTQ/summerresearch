# Finding Complementary Proteins using 3D shape SDFs

Cory Scott summer research group, Colorado College, 2026

Complement search over 3d shapes by treating each shape as a signed distance function and contructing a vantage point tree with those SDFs.

# Goal
Create a database for people upload a protein to find the potential complementary shaped proteins efficiently.

# Idea
Signed distance function can be a way to represent 3D shapes, we used it to represent proteins by treating them as unions of spheres. By taking the l2norm of 2 SDFs, we can compare how similar two 3D shapes are. Then we built a Vantage Point Tree based on SDFs similarities and enabled fast search for k similar shapes. By flipping the sign of the SDF of a shape, we can get its perfect complimentary shape. Using this method we can search for the k complimentary shapes from the VPtree.

# Current Status
Currently we successfully implemented the Vantage Point Tree data sturcture and compliment search function. We are able to upload stl files for simulated protein shapes and correctly getting k similar and complimentary shapes.

# Future work
We are planning to work on applying current work on actual protein dataset, solve the problem of cropping the binding site of proteins and finding the optimal positions in the 3D space for those proteins.
