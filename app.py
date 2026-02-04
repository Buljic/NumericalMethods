"""
NumericalMethods - Main Flask Application (No NumPy needed)
"""

from flask import Flask, render_template, request, jsonify
from methods.lagrange import (
    lagrange_interpolation,
    barycentric_interpolation,
    barycentric_weights,
)
from methods.newton import  newton_divided_differences, newton_interpolation
from methods.spline import cubic_spline_coeffs, cubic_spline_interpolation
from methods.utils import sort_points

app = Flask(__name__, static_folder='static')

# Linearna interpolacija (gotova)
def linear_interpolation(x_points, y_points, x):
    xs, ys = sort_points(x_points, y_points)
    n = len(xs)
    if x <= xs[0]:
        return ys[0] + (x - xs[0]) * (ys[1] - ys[0]) / (xs[1] - xs[0])
    if x >= xs[-1]:
        return ys[-2] + (x - xs[-2]) * (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])

    for i in range(n - 1):
        if xs[i] <= x <= xs[i+1]:
            t = (x - xs[i]) / (xs[i+1] - xs[i])
            return ys[i] + t * (ys[i+1] - ys[i])
    return ys[0]

# Placeholder metode
def newton_interpolation_api(x_points, y_points, x):
    coef = newton_divided_differences(x_points, y_points)
    return newton_interpolation(x_points, y_points, x, coef=coef)

def cubic_spline_interpolation_api(x_points, y_points, x_eval):
    coeffs = cubic_spline_coeffs(x_points, y_points)
    return cubic_spline_interpolation(x_points, y_points, x_eval, coeffs=coeffs)

# Helper funkcija za linspace bez NumPy
def linspace(start, stop, num=200):
    """Simple linspace implementation without NumPy"""
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]

@app.route('/')
def index():
    """Glavna stranica"""
    return render_template('index.html')

@app.route('/interpolate', methods=['POST'])
def interpolate():
    """API endpoint za interpolaciju"""
    try:
        data = request.json
        method = data.get('method', 'lagrange')
        points = data.get('points', [])
        
        if len(points) < 2:
            return jsonify({'error': 'Potrebne su najmanje 2 tačke!'}), 400
        
        # Priprema podataka
        x_points = [float(p['x']) for p in points]
        y_points = [float(p['y']) for p in points]
        
        # Kreiranje x vrijednosti za plot (bez NumPy)
        x_min, x_max = min(x_points), max(x_points)
        x_range = x_max - x_min
        x_plot = linspace(x_min - 0.1*x_range, x_max + 0.1*x_range, 200)
        
        # Odabir metode
        method_names = {
            'lagrange': 'Lagrangeova Interpolacija',
            'barycentric': 'Barycentric Lagrange',
            'newton': 'Newtonova Interpolacija',
            'linear': 'Linearna Interpolacija',
            'spline': 'Kubni Spline'
        }
        
        y_plot = []
        
        if method == 'linear':
            for x in x_plot:
                y_plot.append(linear_interpolation(x_points, y_points, x))
        
        elif method == 'lagrange':
            try:
                for x in x_plot:
                    y_plot.append(lagrange_interpolation(x_points, y_points, x))
            except:
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'

        elif method == 'barycentric':
            try:
                weights = barycentric_weights(x_points)
                for x in x_plot:
                    y_plot.append(barycentric_interpolation(x_points, y_points, x, weights))
            except:
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'
        
        elif method == 'newton':
            try:
                coef = newton_divided_differences(x_points, y_points)
                for x in x_plot:
                   y_plot.append(newton_interpolation(x_points, y_points, x, coef=coef))
            except:
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'
        
        elif method == 'spline':
            try:
                coeffs = cubic_spline_coeffs(x_points, y_points)
                y_plot = cubic_spline_interpolation(x_points, y_points, x_plot, coeffs=coeffs)
                if not isinstance(y_plot, list):
                    y_plot = [float(y_plot)]
            except:
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'
        
        else:
            return jsonify({'error': 'Nepoznata metoda!'}), 400
        
        return jsonify({
            'x_plot': x_plot,
            'y_plot': y_plot,
            'x_points': x_points,
            'y_points': y_points,
            'title': method_names.get(method, 'Interpolacija'),
            'method': method
        })
        
    except Exception as e:
        print(f"Error in interpolate: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("NumericalMethods")
    print("=" * 60)
    print("Flask je instaliran")
    print("Linearna interpolacija radi")
    print("Web aplikacija je spremna")
    print("=" * 60)
    print("Otvori browser: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
