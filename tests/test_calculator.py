"""
Tests für GaubenMaster
======================
"""

import unittest
import sys
import os

# Parent directory zum Pfad hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from GaubenMaster.calculator import TriangleCalculator, get_triangle_properties


class TestGaubenMasterCalculator(unittest.TestCase):
    """Testfälle für Dreiecksberechnungen (GaubenMaster)."""

    def test_validate_triangle_valid(self):
        """Test gültige Dreiecke."""
        self.assertTrue(TriangleCalculator.validate_triangle(3, 4, 5))
        self.assertTrue(TriangleCalculator.validate_triangle(5, 5, 5))
        self.assertTrue(TriangleCalculator.validate_triangle(5, 5, 8))
        self.assertTrue(TriangleCalculator.validate_triangle(10, 10, 10))

    def test_validate_triangle_invalid(self):
        """Test ungültige Dreiecke."""
        self.assertFalse(TriangleCalculator.validate_triangle(1, 2, 3))  # a+b=c
        self.assertFalse(TriangleCalculator.validate_triangle(1, 1, 3))  # a+b<c
        self.assertFalse(TriangleCalculator.validate_triangle(0, 4, 5))  # Null-Seite
        self.assertFalse(
            TriangleCalculator.validate_triangle(-1, 4, 5)
        )  # Negative Seite

    def test_calculate_angles_right_triangle(self):
        """Test 3-4-5 rechtwinkliges Dreieck."""
        alpha, beta, gamma = TriangleCalculator.calculate_angles(3, 4, 5)

        # γ sollte 90° sein (gegenüber Seite c=5)
        self.assertAlmostEqual(gamma, 90.0, places=1)
        # α ≈ 36.87°, β ≈ 53.13°
        self.assertAlmostEqual(alpha, 36.87, places=1)
        self.assertAlmostEqual(beta, 53.13, places=1)
        # Summe = 180°
        self.assertAlmostEqual(alpha + beta + gamma, 180.0, places=1)

    def test_calculate_angles_equilateral(self):
        """Test gleichseitiges Dreieck."""
        alpha, beta, gamma = TriangleCalculator.calculate_angles(5, 5, 5)

        # Alle Winkel 60°
        self.assertAlmostEqual(alpha, 60.0, places=5)
        self.assertAlmostEqual(beta, 60.0, places=5)
        self.assertAlmostEqual(gamma, 60.0, places=5)

    def test_calculate_angles_isosceles(self):
        """Test gleichschenkliges Dreieck."""
        alpha, beta, gamma = TriangleCalculator.calculate_angles(5, 5, 8)

        # Basiswinkel gleich
        self.assertAlmostEqual(alpha, beta, places=5)
        # Summe = 180°
        self.assertAlmostEqual(alpha + beta + gamma, 180.0, places=5)

    def test_calculate_area(self):
        """Test Flächenberechnung."""
        # 3-4-5 Dreieck: Fläche = 6
        area = TriangleCalculator.calculate_area(3, 4, 5)
        self.assertAlmostEqual(area, 6.0, places=5)

        # Gleichseitiges Dreieck a=2: Fläche = sqrt(3)
        area = TriangleCalculator.calculate_area(2, 2, 2)
        import math

        self.assertAlmostEqual(area, math.sqrt(3), places=5)

    def test_calculate_heights(self):
        """Test Höhenberechnung."""
        # 3-4-5 Dreieck
        area = 6.0
        ha, hb, hc = TriangleCalculator.calculate_heights(3, 4, 5, area)

        self.assertAlmostEqual(ha, 4.0, places=5)  # 2*6/3
        self.assertAlmostEqual(hb, 3.0, places=5)  # 2*6/4
        self.assertAlmostEqual(hc, 2.4, places=5)  # 2*6/5

    def test_get_triangle_vertices(self):
        """Test Eckenkoordinaten."""
        A, B, C = TriangleCalculator.get_triangle_vertices(3, 4, 5)

        import numpy as np

        # A bei (0,0), B bei (5,0)
        np.testing.assert_array_almost_equal(A, [0.0, 0.0])
        np.testing.assert_array_almost_equal(B, [5.0, 0.0])

        # C sollte im ersten Quadranten sein
        self.assertGreater(C[0], 0)
        self.assertGreater(C[1], 0)

        # Distanzen prüfen
        self.assertAlmostEqual(np.linalg.norm(B - A), 5.0, places=5)  # c
        self.assertAlmostEqual(np.linalg.norm(C - A), 4.0, places=5)  # b
        self.assertAlmostEqual(np.linalg.norm(C - B), 3.0, places=5)  # a

    def test_get_triangle_properties_complete(self):
        """Test vollständige Eigenschaften."""
        props = get_triangle_properties(3, 4, 5)

        self.assertTrue(props["valid"])
        self.assertEqual(props["sides"], {"a": 3, "b": 4, "c": 5})
        self.assertAlmostEqual(props["angles"]["gamma"], 90.0, places=1)
        self.assertAlmostEqual(props["area"], 6.0, places=5)
        self.assertEqual(props["perimeter"], 12.0)
        self.assertAlmostEqual(props["heights"]["ha"], 4.0, places=5)
        self.assertIn("inradius", props)
        self.assertIn("circumradius", props)

    def test_invalid_triangle_properties(self):
        """Test Eigenschaften bei ungültigem Dreieck."""
        props = get_triangle_properties(1, 2, 3)

        self.assertFalse(props["valid"])
        self.assertIn("error", props)


class TestEdgeCases(unittest.TestCase):
    """Test Randfälle."""

    def test_very_small_triangle(self):
        """Sehr kleines Dreieck."""
        props = get_triangle_properties(0.001, 0.001, 0.001)
        self.assertTrue(props["valid"])
        self.assertAlmostEqual(props["angles"]["alpha"], 60.0, places=1)

    def test_very_large_triangle(self):
        """Sehr großes Dreieck."""
        props = get_triangle_properties(1000000, 1000000, 1000000)
        self.assertTrue(props["valid"])
        self.assertAlmostEqual(props["angles"]["alpha"], 60.0, places=1)

    def test_flat_triangle(self):
        """Fast flaches Dreieck (a+b≈c)."""
        # Gerade noch gültig
        props = get_triangle_properties(1, 2, 2.999)
        self.assertTrue(props["valid"])
        # γ sollte fast 180° sein
        self.assertGreater(props["angles"]["gamma"], 170.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
