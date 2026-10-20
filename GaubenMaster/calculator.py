"""
Dreiecksberechnungs-Modul
=========================

Enthält alle mathematischen Berechnungen für Dreiecke.
"""

import math
import numpy as np
from typing import Tuple, Optional


class TriangleCalculator:
    """Statische Klasse für Dreiecksberechnungen."""
    
    @staticmethod
    def validate_triangle(a: float, b: float, c: float) -> bool:
        """
        Prüft, ob drei Seiten ein gültiges Dreieck bilden.
        
        Dreiecksungleichung: Die Summe je zweier Seiten muss 
        größer als die dritte Seite sein.
        
        Args:
            a, b, c: Seitenlängen
            
        Returns:
            True wenn gültiges Dreieck, sonst False
        """
        if a <= 0 or b <= 0 or c <= 0:
            return False
        return (a + b > c) and (a + c > b) and (b + c > a)
    
    @staticmethod
    def calculate_angles(a: float, b: float, c: float) -> Tuple[float, float, float]:
        """
        Berechnet die Winkel eines Dreiecks aus den Seitenlängen (in Grad).
        Verwendet den Kosinussatz.
        
        Args:
            a, b, c: Seitenlängen
            
        Returns:
            Tuple (alpha, beta, gamma) in Grad
            
        Raises:
            ValueError: Bei ungültigem Dreieck
        """
        if not TriangleCalculator.validate_triangle(a, b, c):
            raise ValueError("Ungültige Dreiecksseiten")
        
        # Winkel alpha (gegenüber Seite a)
        cos_alpha = (b**2 + c**2 - a**2) / (2 * b * c)
        cos_alpha = max(-1.0, min(1.0, cos_alpha))  # Clamping für numerische Stabilität
        alpha = math.degrees(math.acos(cos_alpha))
        
        # Winkel beta (gegenüber Seite b)
        cos_beta = (a**2 + c**2 - b**2) / (2 * a * c)
        cos_beta = max(-1.0, min(1.0, cos_beta))
        beta = math.degrees(math.acos(cos_beta))
        
        # Winkel gamma (gegenüber Seite c)
        gamma = 180.0 - alpha - beta
        
        # Korrektur für Rundungsfehler
        if gamma < 0:
            gamma = 0.0
        
        return alpha, beta, gamma
    
    @staticmethod
    def calculate_area(a: float, b: float, c: float) -> float:
        """
        Berechnet die Fläche nach Heron.
        
        Args:
            a, b, c: Seitenlängen
            
        Returns:
            Fläche in Quadrat-Einheiten
        """
        if not TriangleCalculator.validate_triangle(a, b, c):
            return 0.0
            
        s = (a + b + c) / 2.0
        # Numerische Stabilität: max mit 0
        area_squared = s * (s - a) * (s - b) * (s - c)
        return math.sqrt(max(0.0, area_squared))
    
    @staticmethod
    def calculate_heights(a: float, b: float, c: float, area: float) -> Tuple[float, float, float]:
        """
        Berechnet die Höhen des Dreiecks.
        
        Args:
            a, b, c: Seitenlängen
            area: Fläche des Dreiecks
            
        Returns:
            Tuple (ha, hb, hc) - Höhen auf Seiten a, b, c
        """
        if area <= 0:
            return 0.0, 0.0, 0.0
            
        ha = 2.0 * area / a if a > 0 else 0.0
        hb = 2.0 * area / b if b > 0 else 0.0
        hc = 2.0 * area / c if c > 0 else 0.0
        return ha, hb, hc
    
    @staticmethod
    def get_triangle_vertices(a: float, b: float, c: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Bereitet die Koordinaten der Dreiecksecken vor.
        Platziert Seite c auf der x-Achse von (0,0) nach (c,0).
        
        Convention:
        - Seite a = BC (gegenüber Ecke A)
        - Seite b = CA (gegenüber Ecke B) 
        - Seite c = AB (gegenüber Ecke C, liegt auf x-Achse)
        
        Args:
            a, b, c: Seitenlängen
            
        Returns:
            Tuple (A, B, C) als numpy-Arrays mit [x, y] Koordinaten
        """
        if not TriangleCalculator.validate_triangle(a, b, c):
            raise ValueError("Ungültige Dreiecksseiten für Koordinatenberechnung")
        
        # Koordinaten berechnen:
        # A = (0, 0)
        # B = (c, 0)
        # C = (x, y) mit:
        #   x = (b² + c² - a²) / (2c)  (Projektion von b auf c)
        #   y = √(b² - x²)
        
        x = (b**2 + c**2 - a**2) / (2 * c)
        y_squared = b**2 - x**2
        y = math.sqrt(max(0.0, y_squared))  # Clamping für numerische Stabilität
        
        A = np.array([0.0, 0.0], dtype=float)
        B = np.array([c, 0.0], dtype=float)
        C = np.array([x, y], dtype=float)
        
        return A, B, C
    
    @staticmethod
    def get_triangle_properties(a: float, b: float, c: float) -> dict:
        """
        Berechnet alle Eigenschaften eines Dreiecks auf einmal.
        
        Args:
            a, b, c: Seitenlängen
            
        Returns:
            Dictionary mit allen berechneten Werten
        """
        if not TriangleCalculator.validate_triangle(a, b, c):
            return {
                "valid": False,
                "error": "Dreiecksungleichung verletzt"
            }
        
        alpha, beta, gamma = TriangleCalculator.calculate_angles(a, b, c)
        area = TriangleCalculator.calculate_area(a, b, c)
        perimeter = a + b + c
        ha, hb, hc = TriangleCalculator.calculate_heights(a, b, c, area)
        vertices = TriangleCalculator.get_triangle_vertices(a, b, c)
        
        return {
            "valid": True,
            "sides": {"a": a, "b": b, "c": c},
            "angles": {"alpha": alpha, "beta": beta, "gamma": gamma},
            "area": area,
            "perimeter": perimeter,
            "heights": {"ha": ha, "hb": hb, "hc": hc},
            "vertices": {
                "A": vertices[0].tolist(),
                "B": vertices[1].tolist(),
                "C": vertices[2].tolist()
            },
            "semiperimeter": perimeter / 2.0,
            # Inkreisradius
            "inradius": area / (perimeter / 2.0) if perimeter > 0 else 0.0,
            # Umkreisradius
            "circumradius": (a * b * c) / (4.0 * area) if area > 0 else 0.0,
        }


# Convenience-Funktionen für direkten Import
def validate_triangle(a: float, b: float, c: float) -> bool:
    return TriangleCalculator.validate_triangle(a, b, c)

def calculate_angles(a: float, b: float, c: float) -> Tuple[float, float, float]:
    return TriangleCalculator.calculate_angles(a, b, c)

def calculate_area(a: float, b: float, c: float) -> float:
    return TriangleCalculator.calculate_area(a, b, c)

def get_triangle_properties(a: float, b: float, c: float) -> dict:
    return TriangleCalculator.get_triangle_properties(a, b, c)