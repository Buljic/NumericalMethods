def sort_points(x_points, y_points):
    pts = sorted(zip(x_points, y_points), key=lambda t: t[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return xs, ys

