"""
Tests for the Magnetic Field and field vector computations.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trignum_core.faces import FaceAlpha, FaceBeta, FaceGamma
from trignum_core.magnetic_field import MagneticField, FieldVector


class TestFieldVector(unittest.TestCase):
    """Tests for FieldVector."""

    def test_magnitude(self):
        v = FieldVector(3, 4, 0)
        self.assertAlmostEqual(v.magnitude, 5.0)

    def test_normalized(self):
        v = FieldVector(3, 4, 0)
        n = v.normalized
        self.assertAlmostEqual(n.magnitude, 1.0, places=5)

    def test_zero_vector(self):
        v = FieldVector(0, 0, 0)
        n = v.normalized
        self.assertEqual(n.alpha, 0)

    def test_dominant_face(self):
        v = FieldVector(0.8, 0.1, 0.1)
        self.assertEqual(v.dominant_face, "α (Logic)")

        v = FieldVector(0.1, 0.8, 0.1)
        self.assertEqual(v.dominant_face, "β (Illogic)")

        v = FieldVector(0.1, 0.1, 0.8)
        self.assertEqual(v.dominant_face, "γ (Context)")


class TestMagneticField(unittest.TestCase):
    """Tests for MagneticField."""

    def setUp(self):
        self.alpha = FaceAlpha(1.0)
        self.beta = FaceBeta(1.0)
        self.gamma = FaceGamma(1.0)
        self.field = MagneticField(self.alpha, self.beta, self.gamma)

    def test_compute_field(self):
        vector = self.field.compute_field((0.5, 0.5, 0.5))
        self.assertIsInstance(vector, FieldVector)
        self.assertGreater(vector.magnitude, 0)

    def test_compute_apex(self):
        apex = self.field.compute_apex()
        self.assertIsInstance(apex, FieldVector)

    def test_trillage_path(self):
        path = self.field.get_trillage_path((0.5, 0.5, 0.5), steps=10)
        self.assertEqual(len(path), 11)  # start + 10 steps
        # All positions should be clamped to [0, 1]
        for pos in path:
            for coord in pos:
                self.assertGreaterEqual(coord, 0)
                self.assertLessEqual(coord, 1)

    def test_total_energy(self):
        # Before any computation, energy should be 0
        self.assertEqual(self.field.total_energy, 0.0)
        # After computation, energy should be positive
        self.field.compute_field((0.5, 0.5, 0.5))
        self.assertGreater(self.field.total_energy, 0)

    def test_reset(self):
        self.field.compute_field((0.5, 0.5, 0.5))
        self.field.reset()
        self.assertEqual(self.field.total_energy, 0.0)


if __name__ == "__main__":
    unittest.main()
