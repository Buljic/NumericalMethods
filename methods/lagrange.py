"""
Lagrangeova interpolacija
"""

def lagrange_interpolation(x_points, y_points, x):
    """
    Izračunava vrijednost Lagrangeovog interpolacionog polinoma u tački x
    
    Args:
        x_points: Lista x koordinata tačaka
        y_points: Lista y koordinata tačaka
        x: Tačka u kojoj se evaluira
    
    Returns:
        Interpolirana vrijednost
    """
    # Direct Lagrange formula, O(n^2) per evaluation.
    n = len(x_points)
    eps = 1e-12

    for i in range(n):
        if abs(x - x_points[i]) <= eps:
            return y_points[i]

    total = 0.0
    for i in range(n):
        term = y_points[i]
        xi = x_points[i]
        for j in range(n):
            if i == j:
                continue
            denom = xi - x_points[j]
            if abs(denom) <= eps:
                raise ValueError("Duplicate x value in points.")
            term *= (x - x_points[j]) / denom
        total += term

    return total


def barycentric_weights(x_points):
    # Precompute barycentric weights for stability and speed.
    n = len(x_points)
    eps = 1e-12
    weights = [1.0] * n

    for i in range(n):
        xi = x_points[i]
        prod = 1.0
        for j in range(n):
            if i == j:
                continue
            diff = xi - x_points[j]
            if abs(diff) <= eps:
                raise ValueError("Duplicate x value in points.")
            prod *= diff
        weights[i] = 1.0 / prod

    return weights


def barycentric_interpolation(x_points, y_points, x, weights=None):
    # Evaluate using the first barycentric form.
    if weights is None:
        weights = barycentric_weights(x_points)

    eps = 1e-12
    num = 0.0
    den = 0.0

    for i in range(len(x_points)):
        diff = x - x_points[i]
        if abs(diff) <= eps:
            return y_points[i]
        term = weights[i] / diff
        num += term * y_points[i]
        den += term

    return num / den
