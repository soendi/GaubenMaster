"""
GaubenMaster Package
====================

Ein Paket zur Berechnung und Visualisierung von Dreiecken für den Gaubenbau.
"""

__version__ = "1.0.20"
__author__ = "soendi"
__email__ = "soendi@users.noreply.github.com"
__license__ = "MIT"

from .calculator import TriangleCalculator
from .plot import TrianglePlot
from .update import UpdateManager

__all__ = [
    "TriangleCalculator",
    "TrianglePlot",
    "UpdateManager",
]
