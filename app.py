"""
NumericalMethods - Main Flask Application (No NumPy needed)
"""

from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__, static_folder='static')

# Linearna interpolacija (gotova)
def linear_interpolation(x_points, y_points, x):
    """
    Linearna interpolacija između tačaka
    """
    n = len(x_points)
    
    # Ako je x van opsega
    if x <= x_points[0]:
        return y_points[0]
    
    if x >= x_points[-1]:
        return y_points[-1]
    
    # Pronađi interval
    for i in range(n - 1):
        if x_points[i] <= x <= x_points[i+1]:
            # Linearna interpolacija
            t = (x - x_points[i]) / (x_points[i+1] - x_points[i])
            return y_points[i] + t * (y_points[i+1] - y_points[i])
    
    return y_points[0]  # fallback

# Placeholder metode
def lagrange_interpolation(x_points, y_points, x):
    """TODO: Implementirati Lagrange"""
    return 0.0

def newton_interpolation(x_points, y_points, x):
    """TODO: Implementirati Newton"""
    return 0.0

def cubic_spline_interpolation(x_points, y_points, x_eval):
    """TODO: Implementirati Spline"""
    if isinstance(x_eval, list):
        return [0.0] * len(x_eval)
    return 0.0

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
        
        elif method == 'newton':
            try:
                for x in x_plot:
                    y_plot.append(newton_interpolation(x_points, y_points, x))
            except:
                # Fallback na linearnu
                for x in x_plot:
                    y_plot.append(linear_interpolation(x_points, y_points, x))
                method = 'linear'
        
        elif method == 'spline':
            try:
                y_plot = cubic_spline_interpolation(x_points, y_points, x_plot)
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