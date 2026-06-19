# VPTree implementation for SDFs

# calculate mean squared error between two SDFs over a set of points
def mse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1.func(sdf1, x, y) - sdf2.func(sdf2, x, y)) ** 2
    return (total / len(points))

# VPTree class for organizing SDFs based on their similarity
class VPTree:
    
    def __init__(self, points, sdfs, ucirc):
        self.points = points
        self.sdfs = sdfs
        self.left = None
        self.right = None
        self.ucirc = ucirc

    def split(self):
        if len(self.sdfs) <= 1:
            return
        
        base = self.ucirc
        pivot = self.sdfs[0]
        left_sdfs = []
        right_sdfs = []
        mses = []
        for sdf in self.sdfs:
            mses.append(mse(self.points, base, sdf))
        median_mse = sorted(mses)[len(mses) // 2]
        median_index = mses.index(median_mse)
        
        for sdf in self.sdfs[0:median_index] + self.sdfs[median_index+1:]:
            if mse(self.points, pivot, sdf) < median_mse:
                left_sdfs.append(sdf)
            else:
                right_sdfs.append(sdf)
        
        self.left = VPTree(self.points, left_sdfs, self.ucirc)
        self.right = VPTree(self.points, right_sdfs, self.ucirc)
        
        self.left.split()
        self.right.split()




        
