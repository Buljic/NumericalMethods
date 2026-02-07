"""
Lagrangeova interpolacija

Napomena o razlikama:
- Obicni Lagrange direktno racuna bazne polinome i ima vise mnozenja po evaluaciji.
- Barycentric Lagrange racuna tezine jednom, pa zatim brze i stabilnije evaluira.
"""


def lagrange_interpolation(x_points, y_points, x):
    """
    Izracunava vrijednost Lagrangeovog interpolacionog polinoma u tacki x.

    Args:
        x_points: Lista x koordinata tacaka
        y_points: Lista y koordinata tacaka
        x: Tacka u kojoj se evaluira

    Returns:
        Interpolirana vrijednost
    """
    # Direktna Lagrange formula, O(n^2) po evaluaciji.
    n = len(x_points)
    eps = 1e-12

    for i in range(n):
        # Ako je x tacno na poznatoj tacki, vrati y bez dodatne matematike.
        if abs(x - x_points[i]) <= eps:
            return y_points[i]

    total = 0.0
    for i in range(n):
        # Racunamo vrijednost i-tog baznog polinoma u x.
        term = y_points[i]
        xi = x_points[i]
        for j in range(n):
            if i == j:
                continue
            denom = xi - x_points[j]
            # Provjera duplih x vrijednosti.
            if abs(denom) <= eps:
                raise ValueError("Duplicate x value in points.")
            term *= (x - x_points[j]) / denom
        total += term

    return total


def barycentric_weights(x_points):
    """
    Racuna barycentric tezine za stabilniju evaluaciju.
    """
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
    """
    Evaluacija Lagrange polinoma barycentric formom.
    """
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
