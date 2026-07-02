import heapq
import numpy as np
# VPTree implementation for SDFs

# calculate squred root mean squared error between two SDFs over a set of points
def rmse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1(x, y) - sdf2(x, y)) ** 2
    return (total / len(points)) ** 0.5

# Calculate the L2 norm between two SDFs over a set of points 
def l2norm(points, sdf1, sdf2):
    diff = np.array([sdf1(x, y) - sdf2(x, y) for x, y in points])
    return np.linalg.norm(diff)

# VPTree class for organizing SDFs based on their similarity
class VPTree:
    
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
        if not sdfs:
            return
        # if the number of SDFs is less than or equal to the leaf size, make this node a leaf
        if len(sdfs) <= self.leaf_size:
            self.leaf = sdfs
            self.threshold = 0 # just need something here
            return
        # choose a pivot SDF and calculate the L2 norms to all other SDFs
        self.sdf = sdfs[0]  # choose the first SDF as the pivot
        other_sdfs = sdfs[1:]
        
        l2norms = [l2norm(self.points, self.sdf, sdf) for sdf in other_sdfs]

        # sort the other SDFs based on their L2 norms and find the median to set as the threshold
        order = sorted(range(len(other_sdfs)), key=lambda i: l2norms[i])
        median = len(order) // 2
        self.threshold = l2norms[order[median]]

        # split the other SDFs into two groups based on the threshold
        lower_sdfs = [other_sdfs[i] for i in order[:median]]
        upper_sdfs = [other_sdfs[i] for i in order[median:]]

        # recursively create the near and far subtrees
        if lower_sdfs:
            self.near = VPTree(self.points, lower_sdfs, self.leaf_size)
            self.near.split()
        if upper_sdfs:
            self.far = VPTree(self.points, upper_sdfs, self.leaf_size)
            self.far.split()

# search for the k nearest neighbors of a given SDF in the VPTree
    def searchkNN(self, target_sdf, k):
        # base case1: if the current node is a leaf, return the k nearest neighbors from the leaf
        if self.leaf is not None:
            neighbors = []
            for sdf in self.leaf:
                dist = l2norm(self.points, sdf, target_sdf)
                heapq.heappush_max(neighbors, (dist, sdf.name, sdf))
            while len(neighbors) > k:
                heapq.heappop_max(neighbors)
            return neighbors
        dist = l2norm(self.points, self.sdf, target_sdf)
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
        inverted_target_sdf = lambda x, y: -target_sdf(x, y)
        # base case1: if the current node is a leaf, return the k nearest complements from the leaf
        if self.leaf is not None:
            comps = []
            for sdf in self.leaf:
                dist = l2norm(self.points, sdf, inverted_target_sdf)
                heapq.heappush_max(comps, (dist, sdf.name, sdf))
            while len(comps) > k:
                heapq.heappop_max(comps)
            return comps
        
        dist = l2norm(self.points, self.sdf, inverted_target_sdf)

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
