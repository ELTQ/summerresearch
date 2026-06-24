import heapq
# VPTree implementation for SDFs

# calculate mean squared error between two SDFs over a set of points
def mse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1.func(sdf1, x, y) - sdf2.func(sdf2, x, y)) ** 2
    return (total / len(points))

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
        if not sdfs:
            return
        
        if len(sdfs) <= self.leaf_size:
            self.leaf = sdfs
            self.threshold = 0 # just need something here
            return
        
        self.sdf = sdfs[0]  # choose the first SDF as the pivot
        other_sdfs = sdfs[1:]
        
        mses = [mse(self.points, self.sdf, sdf) for sdf in other_sdfs]

        order = sorted(range(len(other_sdfs)), key=lambda i: mses[i])
        median = len(order) // 2
        self.threshold = mses[order[median]]

        lower_sdfs = [other_sdfs[i] for i in order[:median]]
        upper_sdfs = [other_sdfs[i] for i in order[median:]]

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
                dist = mse(self.points, sdf, target_sdf)
                heapq.heappush_max(neighbors, (dist, sdf))
            while len(neighbors) > k:
                heapq.heappop_max(neighbors)
            return neighbors
        dist = mse(self.points, self.sdf, target_sdf)
        neighbors = []
        heapq.heapify_max(neighbors)
        heapq.heappush_max(neighbors, (dist, self.sdf))

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
        heapq.heapify_max(neighbors)
        while len(neighbors) > k:
                    heapq.heappop_max(neighbors)
        return neighbors
