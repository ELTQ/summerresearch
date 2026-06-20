# VPTree implementation for SDFs

# calculate mean squared error between two SDFs over a set of points
def mse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1.func(sdf1, x, y) - sdf2.func(sdf2, x, y)) ** 2
    return (total / len(points))

# VPTree class for organizing SDFs based on their similarity
class VPTree:
    
    def __init__(self, points, sdfs):
        self.points = points
        self.sdfs = sdfs
        self.sdf = None
        self.threshold = 0.0
        self.left = None
        self.right = None

    def split(self):
        sdfs = self.sdfs
        self.sdfs = None
        if not sdfs:
            return
        
        self.sdf = sdfs[0]  # choose the first SDF as the pivot
        other_sdfs = sdfs[1:]
        if not other_sdfs:
            return
        
        mses = [mse(self.points, self.sdf, sdf) for sdf in other_sdfs]

        order = sorted(range(len(other_sdfs)), key=lambda i: mses[i])
        median = len(order) // 2
        self.threshold = mses[order[median]]

        lower_sdfs = [other_sdfs[i] for i in order[:median]]
        upper_sdfs = [other_sdfs[i] for i in order[median:]]

        if lower_sdfs:
            self.left = VPTree(self.points, lower_sdfs)
            self.left.split()
        if upper_sdfs:
            self.right = VPTree(self.points, upper_sdfs)
            self.right.split()

#search for the k nearest neighbors of a given SDF in the VPTree
    #def search(self, target_sdf, k=1):
