# SDF objects class
class SDF:
    def __init__(self, func):
        self.func = func

    def circle1(x, y, cx = 0.0, cy = 0.0, r = 1.0):
        return ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 - r

    def circle2(x, y, cx = 2.0, cy = 0.0, r = 1.0):
        return ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 - r
