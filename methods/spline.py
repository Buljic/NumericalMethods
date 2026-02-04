"""
Kubni spline interpolacija (Natural cubic spline) - bez NumPy
"""

from methods.utils import sort_points


def cubic_spline_coeffs(x_points, y_points):
    """
    Priprema koeficijente natural cubic spline-a.
    Vraća (xs, a, b, c, d) po intervalima i:
      S_i(x) = a[i] + b[i]*(t) + c[i]*(t^2) + d[i]*(t^3),
      t = x - xs[i], i=0..n-2
    """
    if len(x_points) != len(y_points):
        raise ValueError("x_points i y_points moraju imati istu dužinu.")
    if len(x_points) < 2:
        raise ValueError("Potrebne su najmanje 2 tačke.")

    xs, ys = sort_points(list(x_points), list(y_points))
    n = len(xs)
    eps = 1e-12

    for i in range(1, n):
        if abs(xs[i] - xs[i-1]) <= eps:
            raise ValueError("Duplicate x value in points.")

    # h[i] = x[i+1] - x[i]
    h = [xs[i+1] - xs[i] for i in range(n - 1)]

    # Ako su samo 2 tačke, spline je zapravo linija
    if n == 2:
        a = [ys[0]]
        b = [(ys[1] - ys[0]) / h[0]]
        c = [0.0]
        d = [0.0]
        return xs, a, b, c, d

    # Sastavljanje sistema za c (drugi koeficijent po intervalima)
    # Natural: c0 = cn-1 = 0
    alpha = [0.0] * n
    for i in range(1, n - 1):
        alpha[i] = (3.0 / h[i]) * (ys[i+1] - ys[i]) - (3.0 / h[i-1]) * (ys[i] - ys[i-1])

    # Thomas za tridiagonalni sistem
    l = [0.0] * n
    mu = [0.0] * n
    z = [0.0] * n
    c = [0.0] * n
    b = [0.0] * (n - 1)
    d = [0.0] * (n - 1)
    a = ys[:-1]  # a[i] = y[i]

    l[0] = 1.0
    mu[0] = 0.0
    z[0] = 0.0

    for i in range(1, n - 1):
        l[i] = 2.0 * (xs[i+1] - xs[i-1]) - h[i-1] * mu[i-1]
        if abs(l[i]) <= eps:
            raise ValueError("Degenerate spline system (check x spacing).")
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1] * z[i-1]) / l[i]

    l[n-1] = 1.0
    z[n-1] = 0.0
    c[n-1] = 0.0

    for j in range(n - 2, -1, -1):
        c[j] = z[j] - mu[j] * c[j+1]
        if j < n - 1:
            b[j] = ((ys[j+1] - ys[j]) / h[j]) - (h[j] * (2.0 * c[j] + c[j+1]) / 3.0)
            d[j] = (c[j+1] - c[j]) / (3.0 * h[j])

    # Po intervalima koristimo c[i] (ne treba c[n-1] u evaluaciji)
    c_interval = c[:-1]
    return xs, a, b, c_interval, d

def cubic_spline_interpolation(x_points, y_points, x_eval, coeffs=None):
    """
    Evaluacija natural cubic spline-a.
    x_eval može biti float ili lista.
    """
    if coeffs is None:
        coeffs = cubic_spline_coeffs(x_points, y_points)

    xs, a, b, c, d = coeffs
    n = len(xs)

    def eval_one(x):
        eps = 1e-12

        # Ako je x van opsega -> ekstrapolacija koristeći najbliži interval
        if x <= xs[0]:
            i = 0
        elif x >= xs[-1]:
            i = n - 2
        else:
            # Nađi interval i tako da xs[i] <= x <= xs[i+1]
            # Linearno pretraživanje (OK za male n); može i binary search po želji
            i = 0
            for k in range(n - 1):
                if xs[k] <= x <= xs[k+1]:
                    i = k
                    break

        t = x - xs[i]
        return a[i] + b[i]*t + c[i]*(t**2) + d[i]*(t**3)

    if isinstance(x_eval, (list, tuple)):
        return [eval_one(x) for x in x_eval]
    return eval_one(x_eval)