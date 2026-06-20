# SDF objects class
class SDF:
    def __init__(self, func, cx, cy ): 
        self.func = func
        self.midpoint = (cx, cy)

    def circle(self, x, y, r = 1.0):
        cx = self.midpoint[0]
        cy = self.midpoint[1]
        distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 - r
        return distance
    
    def compare(self, other, points):
        # compare two SDFs 
        total = 0
        for x, y in points:
            total += (self.func(self, x, y) - other.func(other, x, y)) ** 2
        return (total / len(points))