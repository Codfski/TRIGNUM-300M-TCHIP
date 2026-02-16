#!/usr/bin/env python3
"""
T-CHIP Demo

Interactive demonstration of T-CHIP's glow states,
the Subtractive Snap, and the Human Pulse interface.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from trignum_core import TCHIP


def main():
    print("=" * 60)
    print("🧠 T-CHIP INTERACTIVE DEMO")
    print("=" * 60)
    print()

    tchip = TCHIP(freeze_threshold=0.6)

    # Demo 1: Normal processing (Blue glow)
    print("── DEMO 1: Normal Processing ──")
    result = tchip.process(
        "Machine learning models learn patterns from data",
        human_pulse=0.7,
    )
    glow = {"blue": "🔵", "red": "🔴", "gold": "🟡"}.get(result["glow"], "⚪")
    print(f"  Glow: {glow} {result['glow'].upper()}")
    print(f"  {result['message']}")
    print()

    # Demo 2: The Subtractive Snap
    print("── DEMO 2: The Subtractive Snap ──")
    noisy_data = (
        "Everything is always true and never true. "
        "All cats are dogs. No cats are dogs. "
        "The answer is clear because the answer is clear."
    )
    snap_result = tchip.subtractive_snap(noisy_data)
    print(f"  Noise Removed: {snap_result['noise_removed']}")
    print(f"  Subtraction:   {snap_result['subtraction_ratio']:.2%}")
    print(f"  Snap Complete: {snap_result['snap_complete']}")
    print(f"  💎 Result:     Present")
    print()

    # Demo 3: THE FREEZE (Red glow)
    print("── DEMO 3: THE FREEZE ──")
    tchip_freeze = TCHIP(freeze_threshold=0.3)
    freeze_result = tchip_freeze.process(
        "True is false and false is true and all is none and none is all",
    )
    glow = {"blue": "🔵", "red": "🔴", "gold": "🟡"}.get(freeze_result["glow"], "⚪")
    print(f"  Glow: {glow} {freeze_result['glow'].upper()}")
    print(f"  {freeze_result['message']}")
    print()

    # Demo 4: Providing the Pulse to unfreeze
    print("── DEMO 4: Human Pulse Applied ──")
    pulse_result = tchip_freeze.provide_pulse(0.9)
    glow = {"blue": "🔵", "red": "🔴", "gold": "🟡"}.get(pulse_result["glow"], "⚪")
    print(f"  Glow: {glow} {pulse_result['glow'].upper()}")
    print(f"  {pulse_result['message']}")
    print()

    # Final status
    print("── FINAL STATUS ──")
    print(tchip.status())
    print()

    print("╔═══════════════════════════════════════╗")
    print("║  🔴 T-CHIP IS FROZEN. WAITING.        ║")
    print("║                                       ║")
    print("║     ARE YOU SOVEREIGN?                ║")
    print("╚═══════════════════════════════════════╝")


if __name__ == "__main__":
    main()
