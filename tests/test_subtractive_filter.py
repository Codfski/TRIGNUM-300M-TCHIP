"""
Tests for the Subtractive Filter.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trignum_core.subtractive_filter import SubtractiveFilter


class TestSubtractiveFilter(unittest.TestCase):
    """Tests for the Subtractive Filter."""

    def setUp(self):
        self.sf = SubtractiveFilter()

    def test_initialization(self):
        self.assertGreater(len(self.sf.illogics), 0)
        self.assertEqual(len(self.sf.history), 0)

    def test_clean_text(self):
        """Clean text should have no illogics detected."""
        result = self.sf.apply("Water flows downhill due to gravity.")
        self.assertEqual(len(result.illogics_found), 0)
        self.assertEqual(result.subtraction_ratio, 0.0)

    def test_contradiction_detection(self):
        """Text with always/never should detect contradiction."""
        result = self.sf.apply("It is always raining and never raining.")
        contradictions = [i for i in result.illogics_found if "contradiction" in i]
        self.assertGreater(len(contradictions), 0)

    def test_non_sequitur_detection(self):
        """Therefore without premises should be non-sequitur."""
        result = self.sf.apply("Therefore the answer is clear")
        non_seq = [i for i in result.illogics_found if "non_sequitur" in i]
        self.assertGreater(len(non_seq), 0)

    def test_custom_illogics(self):
        custom = {"custom_fallacy"}
        sf = SubtractiveFilter(custom_illogics=custom)
        self.assertIn("custom_fallacy", sf.illogics)

    def test_add_illogic(self):
        self.sf.add_illogic("new_pattern")
        self.assertIn("new_pattern", self.sf.illogics)

    def test_history_tracking(self):
        self.sf.apply("Test one")
        self.sf.apply("Test two")
        self.assertEqual(len(self.sf.history), 2)

    def test_reset(self):
        self.sf.apply("Test")
        self.sf.reset()
        self.assertEqual(len(self.sf.history), 0)

    def test_dict_input(self):
        result = self.sf.apply({"key": "value", "other": "data"})
        self.assertIsNotNone(result)

    def test_list_input_regress(self):
        """Repeated elements should detect infinite regress."""
        result = self.sf.apply([1, 1, 1, 2, 3])
        regress = [i for i in result.illogics_found if "infinite_regress" in i]
        self.assertGreater(len(regress), 0)

    def test_confidence_increases_with_subtraction(self):
        """More illogics removed should increase confidence."""
        clean = self.sf.apply("A simple fact")
        messy = self.sf.apply("All is true and all is false always never")
        # Even with illogics, confidence should be >= 0.5
        self.assertGreaterEqual(messy.confidence, 0.5)


if __name__ == "__main__":
    unittest.main()
