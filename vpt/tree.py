# VPTree implementation for SDFs

# calculate mean squared error between two SDFs over a set of points
from sdflib.sdfs import SDF


def mse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1.func(sdf1, x, y) - sdf2.func(sdf2, x, y)) ** 2
    return (total / len(points))

# VPTree class for organizing SDFs based on their similarity
class VPTree:
    
    def __init__(self, points, sdfs, neutral = SDF(func=SDF.circle, ID=1)):
        self.points = points
        self.sdfs = sdfs # list of SDFs that this node contains
        self.chosen_sdf = None # the SDF that this node contains
        self.left = None # left child node
        self.right = None # right child node
        self.neutral = neutral # the neutral point of comparison. default: unit circle at (0, 0)
        self.difference = -1 # difference from the sdf contained at this node to the neutral sdf
        
    def split(self):
        sdfs = self.sdfs
        self.sdfs = None
        if not sdfs:
            return
        
        base = self.neutral
        left_sdfs = []
        right_sdfs = []
        mses = []
        for sdf in self.sdfs:
            mses.append(mse(self.points, base, sdf))
        median_mse = sorted(mses)[len(mses) // 2]
        median_index = mses.index(median_mse)
        
        for sdf in self.sdfs[0:median_index] + self.sdfs[median_index+1:]:
            if mse(self.points, base, sdf) < median_mse:
                left_sdfs.append(sdf)
            else:
                right_sdfs.append(sdf)
        
        self.left = VPTree(self.points, left_sdfs, self.neutral)
        self.right = VPTree(self.points, right_sdfs, self.neutral)
        
        self.left.split()
        self.right.split()

    def report(self):
        print("Difference is: ", self.difference)
        print("ID is: ", self.sdfs[0].ID)
        print("")


        lower_sdfs = [other_sdfs[i] for i in order[:median]]
        upper_sdfs = [other_sdfs[i] for i in order[median:]]

        if lower_sdfs:
            self.left = VPTree(self.points, lower_sdfs)
            self.left.split()
        if upper_sdfs:
            self.right = VPTree(self.points, upper_sdfs)
            self.right.split()

#search for the k nearest neighbors of a given SDF in the VPTree
    def searchkNN(self, target_sdf, k):
        
        if self.sdf is None:
            return []
        dist = mse(self.points, self.sdf, target_sdf)
        neighbors = [(dist, self.sdf)]

        if dist < self.threshold:
            if self.left is not None:
                neighbors += self.left.searchkNN(target_sdf, k)
                neighbors.sort(key=lambda x: x[0])
                neighbors = neighbors[:k]
            if self.right is not None and (len(neighbors) < k or dist + neighbors[-1][0] >= self.threshold):
                neighbors += self.right.searchkNN(target_sdf, k)

        if dist >= self.threshold:
            if self.right is not None:
                neighbors += self.right.searchkNN(target_sdf, k)
                neighbors.sort(key=lambda x: x[0])
                neighbors = neighbors[:k]
            if self.left is not None and (len(neighbors) < k or dist - neighbors[-1][0] <= self.threshold):
                neighbors += self.left.searchkNN(target_sdf, k)
        neighbors.sort(key=lambda x: x[0])
        return neighbors[:k]
