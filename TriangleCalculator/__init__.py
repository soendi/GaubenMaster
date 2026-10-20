"""
Triangle Calculator Package
===========================

Ein Paket zur Berechnung und Visualisierung von Dreiecken.
"""

__version__ = "1.0.0"
__author__ = "Ihr Name"
__email__ = "ihre.email@example.com"
__license__ = "MIT"

from .calculator import TriangleCalculator
from .plot import TrianglePlot
from .update import UpdateManager

__all__ = [
    "TriangleCalculator",
    "TrianglePlot", 
    "UpdateManager",
]