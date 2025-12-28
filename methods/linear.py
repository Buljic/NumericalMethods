"""
Linearna interpolacija (piecewise)
"""

def linear_interpolation(x_points, y_points, x):
    """
    Linearna interpolacija između tačaka
    
    Args:
        x_points: Lista x koordinata (sortirano)
        y_points: Lista y koordinata
        x: Tačka za evaluaciju
    
    Returns:
        Interpolirana vrijednost
    """
    n = len(x_points)
    
    # Ako je x van opsega, ekstrapoliraj sa prvom/poslednjom dužinom
    if x <= x_points[0]:
        # Ekstrapolacija lijevo
        return y_points[0] + (x - x_points[0]) * (y_points[1] - y_points[0]) / (x_points[1] - x_points[0])
    
    if x >= x_points[-1]:
        # Ekstrapolacija desno
        return y_points[-2] + (x - x_points[-2]) * (y_points[-1] - y_points[-2]) / (x_points[-1] - x_points[-2])
    
    # Pronađi interval
    for i in range(n - 1):
        if x_points[i] <= x <= x_points[i+1]:
            # Linearna interpolacija unutar intervala
            t = (x - x_points[i]) / (x_points[i+1] - x_points[i])
            return y_points[i] + t * (y_points[i+1] - y_points[i])
    
    # Fallback
    return y_points[0]