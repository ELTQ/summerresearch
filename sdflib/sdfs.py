# SDF objects class

import math
import numpy

class SDF:
    def __init__(self, func, cx, cy ): 
        self.func = func
        self.name = "null"

        if self.func == SDF.circle:
            self.name = "Circle"
        elif self.func == SDF.triangle:
            self.name = "Triangle"

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
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))
        
    def __str__(self):
        return (self.name + " at " + str(self.midpoint[0]) + ", " + str(self.midpoint[1]))
    
    # this might be a bad idea, but if two SDFs are ever compared to one another using <, >, =, etc. just return true for anything with equals and false for anything with lt/gt
    def __eq__(self, other):
        return 1
    
    def __lt__(self, other):
        return 0
    
    def __le__(self, other):
        return 1
    
    def __gt__(self, other):
        return 0
    
    def __ge__(self, other):
        return 1