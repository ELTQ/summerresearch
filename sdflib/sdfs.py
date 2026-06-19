# SDF objects class
class SDF:
    def __init__(self, func, ID=0): 
        self.func = func
        self.ID = ID
        match ID: # get some random midpoints 
            case 1: 
                self.midpoint = (0, 1)
            case 2:
                self.midpoint = (1, 0)
            case 3:
                self.midpoint = (3, 4)
            case 4: 
                self.midpoint = (-4, -5)
            case 5:
                self.midpoint = (5, -6)
            case 6:
                self.midpoint = (-2, 4)
            case _: # if ID is not specified, set midpoint to (0, 0)
                self.midpoint = (0, 0)

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