#!/usr/bin/env python3
"""
Basic Usage Example for TRIGNUM-300M

Demonstrates the fundamental concepts of the Trignum framework.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from trignum_core import TrignumPyramid, TCHIP


def main():
    print("=" * 60)
    print("🔺 TRIGNUM-300M: Basic Usage Example")
    print("=" * 60)
    print()

    # 1. Initialize the Trignum Pyramid
    print("1. Initializing Trignum Pyramid...")
    pyramid = TrignumPyramid()
    print(f"   {pyramid}")
    print()

    # 2. Process simple data
    print("2. Processing data through Magnetic Trillage...")
    result = pyramid.process("The sun rises in the east", human_pulse=0.9)
    print(f"   Logic:      {result.logic_component:.3f}")
    print(f"   Illogic:    {result.illogic_component:.3f}")
    print(f"   Context:    {result.context_component:.3f}")
    print(f"   State:      {result.state.value}")
    print(f"   Confidence: {result.confidence:.2%}")
    print()

    # 3. Initialize T-CHIP
    print("3. Initializing T-CHIP...")
    tchip = TCHIP()
    print(f"   {tchip}")
    print()

    # 4. Process through T-CHIP
    print("4. Processing through T-CHIP...")
    output = tchip.process(
        "Quantum computing uses superposition of qubits",
        human_pulse=0.8,
    )
    print(f"   Glow:       {output['glow']}")
    print(f"   Vibration:  {output['vibration']}")
    print(f"   Message:    {output['message']}")
    print(f"   Confidence: {output['confidence']:.2%}")
    print()

    # 5. Trigger THE FREEZE
    print("5. Triggering THE FREEZE with contradictory data...")
    pyramid_freeze = TrignumPyramid(freeze_threshold=0.3)
    freeze_result = pyramid_freeze.process(
        "Everything is always true and always false and never exists"
    )
    print(f"   State: {freeze_result.state.value}")
    if freeze_result.freeze_coordinates:
        print(f"   Freeze Coordinates: {freeze_result.freeze_coordinates}")
    if freeze_result.metadata.get("message"):
        print(f"   Message: {freeze_result.metadata['message']}")
    print()

    # 6. Display T-CHIP status
    print("6. T-CHIP Status:")
    print(tchip.status())
    print()

    print("💎 Basic usage complete. Are you Sovereign?")


if __name__ == "__main__":
    main()
