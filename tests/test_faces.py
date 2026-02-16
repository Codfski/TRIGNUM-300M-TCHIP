"""
Tests for the Three Faces (α, β, γ) of the Trignum Pyramid.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trignum_core.faces import FaceAlpha, FaceBeta, FaceGamma


class TestFaceAlpha(unittest.TestCase):
    """Tests for Face α — The Logic Pole."""

    def setUp(self):
        self.face = FaceAlpha(strength=1.0)

    def test_initialization(self):
        self.assertEqual(self.face.strength, 1.0)
        self.assertEqual(self.face.COLOR, "blue")
        self.assertEqual(self.face.SYMBOL, "α")

    def test_attraction_low_entropy(self):
        """Low entropy data should attract strongly to Logic."""
        data = {"entropy": 1.0, "length": 10, "tokens": ["hello"]}
        attraction = self.face.attract(data)
        self.assertGreater(attraction, 0.5)

    def test_attraction_high_entropy(self):
        """High entropy data should attract weakly to Logic."""
        data = {"entropy": 7.0, "length": 10, "tokens": ["hello"]}
        attraction = self.face.attract(data)
        self.assertLess(attraction, 0.5)

    def test_strength_clamping(self):
        face = FaceAlpha(strength=5.0)
        self.assertEqual(face.strength, 2.0)
        face = FaceAlpha(strength=-1.0)
        self.assertEqual(face.strength, 0.0)

    def test_reset(self):
        self.face.attract({"entropy": 1.0, "length": 5})
        self.face.reset()
        self.assertEqual(self.face._cycles, 0)


class TestFaceBeta(unittest.TestCase):
    """Tests for Face β — The Illogic Pole."""

    def setUp(self):
        self.face = FaceBeta(strength=1.0)

    def test_initialization(self):
        self.assertEqual(self.face.COLOR, "red")
        self.assertEqual(self.face.SYMBOL, "β")
        self.assertFalse(self.face.is_vacuum_active)

    def test_attraction_high_entropy(self):
        """High entropy data should attract strongly to Illogic."""
        data = {"entropy": 7.0, "length": 10}
        attraction = self.face.attract(data)
        self.assertGreater(attraction, 0.5)

    def test_vacuum_creation(self):
        """Vacuum should activate when create_vacuum is called."""
        vacuum = self.face.create_vacuum(0.8)
        self.assertTrue(self.face.is_vacuum_active)
        self.assertGreater(vacuum, 0)
        self.assertLessEqual(vacuum, 1.0)

    def test_reset(self):
        self.face.create_vacuum(0.5)
        self.face.reset()
        self.assertFalse(self.face.is_vacuum_active)


class TestFaceGamma(unittest.TestCase):
    """Tests for Face γ — The Context / Human Pulse Pole."""

    def setUp(self):
        self.face = FaceGamma(strength=1.0)

    def test_initialization(self):
        self.assertEqual(self.face.COLOR, "gold")
        self.assertEqual(self.face.SYMBOL, "γ")
        self.assertFalse(self.face.is_pulse_active)

    def test_pulse_application(self):
        """Pulse should activate and store value."""
        self.face.apply_pulse(0.8)
        self.assertTrue(self.face.is_pulse_active)
        self.assertAlmostEqual(self.face.pulse_value, 0.8)

    def test_pulse_clamping(self):
        """Pulse should be clamped to [0, 1]."""
        self.face.apply_pulse(5.0)
        self.assertEqual(self.face.pulse_value, 1.0)
        self.face.apply_pulse(-1.0)
        self.assertEqual(self.face.pulse_value, 0.0)

    def test_attraction_moderate_entropy(self):
        """Moderate entropy should attract most to Context."""
        data = {"entropy": 4.0, "length": 10, "tokens": list("abcdefghij")}
        attraction = self.face.attract(data)
        self.assertGreater(attraction, 0)

    def test_reset(self):
        self.face.apply_pulse(0.9)
        self.face.reset()
        self.assertFalse(self.face.is_pulse_active)
        self.assertEqual(self.face.pulse_value, 0.0)


if __name__ == "__main__":
    unittest.main()
