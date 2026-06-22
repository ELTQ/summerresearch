# SDF objects class

import math
import numpy

class SDF:
    def __init__(self, func, cx, cy ): 
        self.func = func
        self.midpoint = (cx, cy)

    def circle(self, x, y, r = 1.0):
        cx = self.midpoint[0]
        cy = self.midpoint[1]
        distance = math.dist((cx, cy), (x, y)) - r
        return distance
    
    def triangle(self, x, y, r = 1.0):
        cx = self.midpoint[0]
        cy = self.midpoint[1]

        k = math.sqrt(3.0) # number of sides?
        x = abs(x) - r
        y = abs(y) + r/k
        if (((x + k) * y) > 0):
            x = ((x-k)*y) / 2
            y = ((-k*x)-y) / 2
        x -= numpy.clip(x, -2*r, 0)
        return -math.dist((cx, cy), (x, y)) * math.copysign(1, y) # we dont have a sign function so this is what i need to do instead
    
    def compare(self, other, points):
        # compare two SDFs 
        total = 0
        for x, y in points:
            total += (self.func(self, x, y) - other.func(other, x, y)) ** 2
        return (total / len(points))
    
    def report(self):
        #print("Function is, " + self.func.__name__ + "()")
        #print("Midpoint is, ", self.midpoint[0], ", ",  self.midpoint[1] )
        return (self.func.__name__ + "() at ", "(", self.midpoint[0], "," , self.midpoint[1], ")")