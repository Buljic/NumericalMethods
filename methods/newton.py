"""
Newtonova interpolacija sa podijeljenim razlikama
"""

from methods.utils import sort_points


def newton_divided_differences(x_points, y_points):
    """
    Računa koeficijente Newtonovog polinoma (podijeljene razlike).
    Vraća listu koeficijenata a[0..n-1] gdje je:
      P(x) = a0 + a1(x-x0) + a2(x-x0)(x-x1) + ...
    """
    if len(x_points) != len(y_points):
        raise ValueError("x_points i y_points moraju imati istu dužinu.")
    if len(x_points) < 2:
        raise ValueError("Potrebne su najmanje 2 tačke.")

    xs, ys = sort_points(list(x_points), list(y_points))
    n = len(xs)
    eps = 1e-12

    # Provjera duplih x
    for i in range(1, n):
        if abs(xs[i] - xs[i-1]) <= eps:
            raise ValueError("Duplicate x value in points.")

    # Kopija y kao prva kolona tablice
    coef = ys[:]  # coef će se na kraju pretvoriti u a[i]
    # In-place računanje podijeljenih razlika:
    # nakon k-te iteracije, coef[i] = f[x_i, ..., x_{i+k}]
    for k in range(1, n):
        for i in range(n - 1, k - 1, -1):
            denom = xs[i] - xs[i - k]
            if abs(denom) <= eps:
                raise ValueError("Duplicate x value in points.")
            coef[i] = (coef[i] - coef[i - 1]) / denom

    # coef[0] je a0, coef[1] je a1, ...
    return coef

def newton_interpolation(x_points, y_points, x, coef=None):
    """
    Evaluacija Newtonovog interpolacionog polinoma u tački x.
    Ako se radi više evaluacija za iste tačke, proslijedi coef=newton_divided_differences(...)
    """
    xs, ys = sort_points(list(x_points), list(y_points))
    if coef is None:
        coef = newton_divided_differences(xs, ys)

    n = len(xs)
    eps = 1e-12

    # Ako je x baš neka od tačaka:
    for i in range(n):
        if abs(x - xs[i]) <= eps:
            return ys[i]

    # Horner-like evaluacija za Newton oblik
    result = coef[-1]
    for i in range(n - 2, -1, -1):
        result = result * (x - xs[i]) + coef[i]
    return result