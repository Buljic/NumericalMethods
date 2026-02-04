"""
NumericalMethods - Main Flask Application
"""

from flask import Flask, render_template, request, jsonify
from methods.lagrange import (
    lagrange_interpolation,
    barycentric_interpolation,
    barycentric_weights,
)
from methods.newton import newton_divided_differences, newton_interpolation
from methods.spline import cubic_spline_coeffs, cubic_spline_interpolation
from methods.linear import linear_interpolation
from methods.utils import sort_points

app = Flask(__name__, static_folder='static')


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
        
        # Kreiranje x vrijednosti za plot
        x_min, x_max = min(x_points), max(x_points)
        x_range = x_max - x_min
        x_plot = linspace(x_min - 0.1*x_range, x_max + 0.1*x_range, 200)
        
        # Nazivi metoda
        method_names = {
            'lagrange': 'Lagrangeova Interpolacija',
            'barycentric': 'Barycentric Lagrange',
            'newton': 'Newtonova Interpolacija',
            'linear': 'Linearna Interpolacija',
            'spline': 'Kubni Spline'
        }
        
        y_plot = []
        
        # Izaberi metodu i računaj
        if method == 'linear':
            for x in x_plot:
                y_plot.append(linear_interpolation(x_points, y_points, x))
        
        elif method == 'lagrange':
            try:
                for x in x_plot:
                    y_plot.append(lagrange_interpolation(x_points, y_points, x))
            except Exception as e:
                print(f"Lagrange greška: {e}")
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'

        elif method == 'barycentric':
            try:
                weights = barycentric_weights(x_points)
                for x in x_plot:
                    y_plot.append(barycentric_interpolation(x_points, y_points, x, weights))
            except Exception as e:
                print(f"Barycentric greška: {e}")
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'
        
        elif method == 'newton':
            try:
                coef = newton_divided_differences(x_points, y_points)
                for x in x_plot:
                    y_plot.append(newton_interpolation(x_points, y_points, x, coef=coef))
            except Exception as e:
                print(f"Newton greška: {e}")
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'
        
        elif method == 'spline':
            try:
                coeffs = cubic_spline_coeffs(x_points, y_points)
                y_plot = cubic_spline_interpolation(x_points, y_points, x_plot, coeffs=coeffs)
                # cubic_spline_interpolation već vraća listu
                if not isinstance(y_plot, list):
                    y_plot = [float(y_plot)]
            except Exception as e:
                print(f"Spline greška: {e}")
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
    print("NumericalMethods - Fakultetski projekat")
    print("=" * 60)
    print("✓ Flask instaliran")
    print("✓ Sve metode implementirane")
    print("✓ Web aplikacija spremna")
    print("=" * 60)
    print("Otvori browser: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)