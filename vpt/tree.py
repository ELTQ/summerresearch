import heapq
import numpy as np
from scipy.integrate import quad,dblquad,qmc_quad
from tqdm import tqdm

# VPTree implementation for SDFs

# calculate squred root mean squared error between two SDFs over a set of points
def rmse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1(x, y) - sdf2(x, y)) ** 2
    return (total / len(points)) ** 0.5

# Calculate the L2 norm between two SDFs over a set of points
def l2norm(sdf1, sdf2):
    quad_func = lambda x: np.power((sdf1(x.T) - sdf2(x.T)),2.0).reshape(-1)
    #integral, error = dblquad(quad_func, lb, ub, lambda x: lb, lambda x: ub, epsabs=.1)
    integral, error = qmc_quad(quad_func, np.zeros(2), np.ones(2), n_points=1e3)
    print(error)
    return np.sqrt(integral)

def l2norm3d(sdf1, sdf2):
    quad_func = lambda x: np.power((sdf1(np.atleast_2d(x.T)) - sdf2(np.atleast_2d(x.T))),2.0).reshape(-1)
    integral, error = qmc_quad(quad_func, np.zeros(3), np.ones(3), n_points=1e3)
    print(error)
    return np.sqrt(integral)

class VPTree:

    def __init__(self, sdfs, leaf_size=1):
        self.sdfs = sdfs
        self.leaf_size = leaf_size
        self.leaf = None
        self.sdf = None
        self.threshold = -1
        self.near = None
        self.far = None


    def split(self):
        sdfs = self.sdfs
        self.sdfs = None
        # if there are no SDFs, return
        if len(sdfs) == 0:
            print('break')
            return
        # if the number of SDFs is less than or equal to the leaf size, make this node a leaf
        if len(sdfs) <= self.leaf_size:
            self.leaf = sdfs
            self.threshold = 0 # just need something here
            return
        # choose a pivot SDF and calculate the L2 norms to all other SDFs
        self.sdf = sdfs[0]  # choose the first SDF as the pivot, it may be more optimal to choose another
        other_sdfs = sdfs[1:]

        print(len(other_sdfs))
        l2norms = [l2norm3d(self.sdf, sdf) for sdf in tqdm(other_sdfs)]

        # sort the other SDFs based on their L2 norms and find the median to set as the threshold
        order = sorted(range(len(other_sdfs)), key=lambda i: l2norms[i])
        median = len(order) // 2
        self.threshold = l2norms[order[median]]

        # split the other SDFs into two groups based on the threshold
        lower_sdfs = [other_sdfs[i] for i in order[:median]]
        upper_sdfs = [other_sdfs[i] for i in order[median:]]

        # recursively create the near and far subtrees
        if lower_sdfs:
            self.near = VPTree(lower_sdfs, self.leaf_size)
            self.near.split()
        if upper_sdfs:
            self.far = VPTree(upper_sdfs, self.leaf_size)
            self.far.split()

# search for the k nearest neighbors of a given SDF in the VPTree
    def searchkNN(self, target_sdf, k):
        # base case1: if the current node is a leaf, return the k nearest neighbors from the leaf
        if self.leaf is not None:
            neighbors = []
            for sdf in self.leaf:
                dist = l2norm3d(sdf, target_sdf)
                heapq.heappush_max(neighbors, (dist, sdf.name, sdf))
            while len(neighbors) > k:
                heapq.heappop_max(neighbors)
            return neighbors
        dist = l2norm3d(self.sdf, target_sdf)
        # list of nearest neighbors found so far
        neighbors = []
        # pushing the current node's SDF onto the heap
        heapq.heappush_max(neighbors, (dist, self.sdf.name, self.sdf))

        # vptree querying logic
        if dist < self.threshold:
            if self.near is not None:
                neighbors.extend(self.near.searchkNN(target_sdf, k))
                heapq.heapify_max(neighbors)
                while len(neighbors) > k:
                    heapq.heappop_max(neighbors)
            if self.far is not None and (len(neighbors) < k or dist + neighbors[0][0] >= self.threshold):
                neighbors.extend(self.far.searchkNN(target_sdf, k))

        if dist >= self.threshold:
            if self.far is not None:
                neighbors.extend(self.far.searchkNN(target_sdf, k))
                heapq.heapify_max(neighbors)
                while len(neighbors) > k:
                    heapq.heappop_max(neighbors)
            if self.near is not None and (len(neighbors) < k or dist - neighbors[0][0] <= self.threshold):
                neighbors.extend(self.near.searchkNN(target_sdf, k))
        # heapify the neighbors list and pop elements until only k remain
        heapq.heapify_max(neighbors)
        while len(neighbors) > k:
                    heapq.heappop_max(neighbors)
        # return the k nearest neighbors
        return neighbors



    # search for the k nearest complements of a given SDF in the VPTree
    def searchkcomp(self, target_sdf, k):
        inverted_target_sdf = lambda arr: -1*target_sdf(arr)
        # base case1: if the current node is a leaf, return the k nearest complements from the leaf
        if self.leaf is not None:
            comps = []
            for sdf in self.leaf:
                dist = l2norm3d(sdf, inverted_target_sdf)
                heapq.heappush_max(comps, (dist, sdf.name, sdf))
            while len(comps) > k:
                heapq.heappop_max(comps)
            return comps

        dist = l2norm3d(self.sdf, inverted_target_sdf)

        # list of complementary SDFs found so far
        comps = []
        # pushing the current node's SDF onto the heap
        heapq.heappush_max(comps, (dist, self.sdf.name, self.sdf))

        # vptree querying logic
        if dist < self.threshold:
            if self.near is not None:
                comps.extend(self.near.searchkcomp(target_sdf, k))
                heapq.heapify_max(comps)
                while len(comps) > k:
                    heapq.heappop_max(comps)
            if self.far is not None and (len(comps) < k or dist + comps[0][0] >= self.threshold):
                comps.extend(self.far.searchkcomp(target_sdf, k))

        if dist >= self.threshold:
            if self.far is not None:
                comps.extend(self.far.searchkcomp(target_sdf, k))
                heapq.heapify_max(comps)
                while len(comps) > k:
                    heapq.heappop_max(comps)
            if self.near is not None and (len(comps) < k or dist - comps[0][0] <= self.threshold):
                comps.extend(self.near.searchkcomp(target_sdf, k))

        # heapify the comps list and pop elements until only k remain
        heapq.heapify_max(comps)
        while len(comps) > k:
                heapq.heappop_max(comps)
        # return the k nearest complements
        return comps
    

class VPTree_2D:

    def __init__(self, points, sdfs, leaf_size=1):
        self.points = points
        self.sdfs = sdfs
        self.leaf_size = leaf_size
        self.leaf = None
        self.sdf = None
        self.threshold = -1
        self.near = None
        self.far = None


    def split(self):
        sdfs = self.sdfs
        self.sdfs = None
        # if there are no SDFs, return
        if len(sdfs) == 0:
            print('break')
            return
        # if the number of SDFs is less than or equal to the leaf size, make this node a leaf
        if len(sdfs) <= self.leaf_size:
            self.leaf = sdfs
            self.threshold = 0 # just need something here
            return
        # choose a pivot SDF and calculate the L2 norms to all other SDFs
        self.sdf = sdfs[0]  # choose the first SDF as the pivot
        other_sdfs = sdfs[1:]

        print(len(other_sdfs))
        l2norms = [l2norm(self.sdf, sdf) for sdf in tqdm(other_sdfs)]

        # sort the other SDFs based on their L2 norms and find the median to set as the threshold
        order = sorted(range(len(other_sdfs)), key=lambda i: l2norms[i])
        median = len(order) // 2
        self.threshold = l2norms[order[median]]

        # split the other SDFs into two groups based on the threshold
        lower_sdfs = [other_sdfs[i] for i in order[:median]]
        upper_sdfs = [other_sdfs[i] for i in order[median:]]

        # recursively create the near and far subtrees
        if lower_sdfs:
            self.near = VPTree_2D(self.points, lower_sdfs, self.leaf_size)
            self.near.split()
        if upper_sdfs:
            self.far = VPTree_2D(self.points, upper_sdfs, self.leaf_size)
            self.far.split()

# search for the k nearest neighbors of a given SDF in the VPTree
    def searchkNN(self, target_sdf, k):
        # base case1: if the current node is a leaf, return the k nearest neighbors from the leaf
        if self.leaf is not None:
            neighbors = []
            for sdf in self.leaf:
                dist = l2norm(sdf, target_sdf)
                heapq.heappush_max(neighbors, (dist, sdf.name, sdf))
            while len(neighbors) > k:
                heapq.heappop_max(neighbors)
            return neighbors
        dist = l2norm(self.sdf, target_sdf)
        # list of nearest neighbors found so far
        neighbors = []
        # pushing the current node's SDF onto the heap
        heapq.heappush_max(neighbors, (dist, self.sdf.name, self.sdf))

        # vptree querying logic
        if dist < self.threshold:
            if self.near is not None:
                neighbors.extend(self.near.searchkNN(target_sdf, k))
                heapq.heapify_max(neighbors)
                while len(neighbors) > k:
                    heapq.heappop_max(neighbors)
            if self.far is not None and (len(neighbors) < k or dist + neighbors[0][0] >= self.threshold):
                neighbors.extend(self.far.searchkNN(target_sdf, k))

        if dist >= self.threshold:
            if self.far is not None:
                neighbors.extend(self.far.searchkNN(target_sdf, k))
                heapq.heapify_max(neighbors)
                while len(neighbors) > k:
                    heapq.heappop_max(neighbors)
            if self.near is not None and (len(neighbors) < k or dist - neighbors[0][0] <= self.threshold):
                neighbors.extend(self.near.searchkNN(target_sdf, k))
        # heapify the neighbors list and pop elements until only k remain
        heapq.heapify_max(neighbors)
        while len(neighbors) > k:
                    heapq.heappop_max(neighbors)
        # return the k nearest neighbors
        return neighbors



    # search for the k nearest complements of a given SDF in the VPTree
    def searchkcomp(self, target_sdf, k):
        inverted_target_sdf = lambda arr: -1*target_sdf(arr)
        # base case1: if the current node is a leaf, return the k nearest complements from the leaf
        if self.leaf is not None:
            comps = []
            for sdf in self.leaf:
                dist = l2norm(sdf, inverted_target_sdf)
                heapq.heappush_max(comps, (dist, sdf.name, sdf))
            while len(comps) > k:
                heapq.heappop_max(comps)
            return comps

        dist = l2norm(self.sdf, inverted_target_sdf)

        # list of complementary SDFs found so far
        comps = []
        # pushing the current node's SDF onto the heap
        heapq.heappush_max(comps, (dist, self.sdf.name, self.sdf))

        # vptree querying logic
        if dist < self.threshold:
            if self.near is not None:
                comps.extend(self.near.searchkcomp(target_sdf, k))
                heapq.heapify_max(comps)
                while len(comps) > k:
                    heapq.heappop_max(comps)
            if self.far is not None and (len(comps) < k or dist + comps[0][0] >= self.threshold):
                comps.extend(self.far.searchkcomp(target_sdf, k))

        if dist >= self.threshold:
            if self.far is not None:
                comps.extend(self.far.searchkcomp(target_sdf, k))
                heapq.heapify_max(comps)
                while len(comps) > k:
                    heapq.heappop_max(comps)
            if self.near is not None and (len(comps) < k or dist - comps[0][0] <= self.threshold):
                comps.extend(self.near.searchkcomp(target_sdf, k))

        # heapify the comps list and pop elements until only k remain
        heapq.heapify_max(comps)
        while len(comps) > k:
                heapq.heappop_max(comps)
        # return the k nearest complements
        return comps