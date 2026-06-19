

def mse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1.func(sdf1, x, y) - sdf2.func(sdf2, x, y)) ** 2
    return (total / len(points))

class VPTree:
    
    def __init__(self, points, sdfs):
        self.points = points
        self.sdfs = sdfs
        self.left = None
        self.right = None

    def split(self):
        if len(self.sdfs) <= 1:
            return
        
        pivot = self.sdfs[0]
        left_sdfs = []
        right_sdfs = []
        
        for sdf in self.sdfs[1:]:
            if mse(self.points, pivot, sdf) < mse(self.points, pivot, self.sdfs[-1]):
                left_sdfs.append(sdf)
            else:
                right_sdfs.append(sdf)
        
        self.left = VPTree(self.points, left_sdfs)
        self.right = VPTree(self.points, right_sdfs)
        
        self.left.split()
        self.right.split()




        
