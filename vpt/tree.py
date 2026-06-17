def mse(points, sdf1, sdf2):
    total = 0
    for x, y in points:
        total += (sdf1.func(x, y) - sdf2.func(x, y)) ** 2
    return total / len(points)
