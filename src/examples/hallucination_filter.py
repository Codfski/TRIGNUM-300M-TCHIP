#!/usr/bin/env python3
"""
Hallucination Filter Example

Demonstrates the Subtractive Filter detecting and isolating
Illogics (hallucinations) from data.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from trignum_core import SubtractiveFilter


def main():
    print("=" * 60)
    print("🔴 HALLUCINATION FILTER DEMO")
    print("=" * 60)
    print()

    sf = SubtractiveFilter()

    # Test cases with varying levels of Illogic
    test_cases = [
        {
            "label": "Clean Logic",
            "data": "Water flows downhill due to gravity. Temperature affects molecular motion.",
        },
        {
            "label": "Contradiction Present",
            "data": "The temperature is always cold. The temperature is never cold. Therefore it is warm.",
        },
        {
            "label": "Circular Reference",
            "data": "The answer is X because of Y. The answer is X because of Z. The answer is X because of Y.",
        },
        {
            "label": "Non-Sequitur",
            "data": "Therefore the conclusion is obvious.",
        },
        {
            "label": "Complex Mixed",
            "data": "All particles have mass. No particles have mass. Some particles are always moving and never at rest. Thus we conclude everything.",
        },
    ]

    for case in test_cases:
        print(f"  📝 {case['label']}")
        print(f"     Input: \"{case['data'][:60]}...\"")

        result = sf.apply(case["data"])

        print(f"     Illogics Found: {len(result.illogics_found)}")
        for il in result.illogics_found:
            print(f"       ❌ {il}")
        print(f"     Subtraction Ratio: {result.subtraction_ratio:.2%}")
        print(f"     Confidence: {result.confidence:.2%}")
        print()

    print(f"  Filter Stats: {sf}")
    print()
    print("  💎 Noise In, Truth Out — The Subtractive Snap.")


if __name__ == "__main__":
    main()
