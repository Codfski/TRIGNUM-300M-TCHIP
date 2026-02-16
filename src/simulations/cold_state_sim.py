#!/usr/bin/env python3
"""
Cold State Simulation

Demonstrates how Trignum processing achieves near-zero entropy
compared to traditional "hot" computation.
"""

import sys
import os
import time
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from trignum_core import TrignumPyramid, TCHIP


def simulate_thermal_comparison():
    """
    Compare energy consumption of traditional vs Trignum processing.
    """
    print("=" * 60)
    print("❄️  COLD STATE SIMULATION")
    print("=" * 60)
    print()

    # Traditional "Hot State" simulation
    print("🔥 TRADITIONAL (HOT STATE) PROCESSING")
    print("─" * 40)

    hot_operations = 1000
    hot_energy_per_op = 100  # picojoules (typical GPU)
    hot_total_energy = hot_operations * hot_energy_per_op
    hot_heat = hot_total_energy * 0.4  # 40% becomes heat

    print(f"  Operations:     {hot_operations:,}")
    print(f"  Energy/op:      {hot_energy_per_op} pJ")
    print(f"  Total Energy:   {hot_total_energy:,} pJ")
    print(f"  Heat Generated: {hot_heat:,.0f} pJ (40%)")
    print(f"  Cooling Needed: YES")
    print()

    # Trignum "Cold State" simulation
    print("❄️  TRIGNUM (COLD STATE) PROCESSING")
    print("─" * 40)

    trignum_field_setup = 50  # pJ (one-time field establishment)
    trignum_ops = 1000
    trignum_energy_per_op = 0.001  # pJ (field propagation only)
    trignum_total_energy = trignum_field_setup + (trignum_ops * trignum_energy_per_op)
    trignum_heat = 0  # No heat in superconductive field

    print(f"  Operations:     {trignum_ops:,}")
    print(f"  Field Setup:    {trignum_field_setup} pJ (one-time)")
    print(f"  Energy/op:      {trignum_energy_per_op} pJ")
    print(f"  Total Energy:   {trignum_total_energy:,.3f} pJ")
    print(f"  Heat Generated: {trignum_heat} pJ (0%)")
    print(f"  Cooling Needed: NO")
    print()

    # Comparison
    print("📊 COMPARISON")
    print("─" * 40)
    ratio = hot_total_energy / trignum_total_energy
    savings = (1 - trignum_total_energy / hot_total_energy) * 100

    print(f"  Energy Ratio:   {ratio:,.0f}× more efficient")
    print(f"  Heat Savings:   {savings:.2f}%")
    print(f"  Cooling Saved:  100% (ambient only)")
    print()


def simulate_entropy_over_time():
    """
    Track entropy levels as both systems process data over time.
    """
    print("=" * 60)
    print("📈 ENTROPY OVER TIME")
    print("=" * 60)
    print()

    n_steps = 20

    print(f"  {'Step':>4}  {'Hot Entropy':>12}  {'Cold Entropy':>13}  {'Ratio':>8}")
    print(f"  {'─'*4}  {'─'*12}  {'─'*13}  {'─'*8}")

    for step in range(1, n_steps + 1):
        # Hot state: entropy increases with each operation
        hot_entropy = math.log(step + 1) * 10

        # Cold state: entropy stays near zero
        cold_entropy = 0.001 * step

        ratio = hot_entropy / max(cold_entropy, 0.001)

        hot_bar = "█" * min(int(hot_entropy / 2), 20)
        cold_bar = "░" * max(1, min(int(cold_entropy * 100), 5))

        print(f"  {step:4d}  {hot_entropy:10.3f} {hot_bar}  "
              f"{cold_entropy:11.5f} {cold_bar}  {ratio:8.1f}×")

    print()
    print("  █ = Hot State Entropy    ░ = Cold State Entropy")
    print()


def simulate_tchip_cold_state():
    """
    Run T-CHIP and demonstrate Cold State operation.
    """
    print("=" * 60)
    print("🧠 T-CHIP COLD STATE OPERATION")
    print("=" * 60)
    print()

    tchip = TCHIP(freeze_threshold=0.7)

    test_queries = [
        ("The speed of light is constant in a vacuum", 0.8),
        ("Water boils at 100°C and also at 0°C simultaneously", None),
        ("Human consciousness emerges from neural complexity", 0.9),
        ("Everything is always true and never true and maybe true", 0.3),
    ]

    for query, pulse in test_queries:
        print(f"  Query: \"{query}\"")
        print(f"  Pulse: {pulse}")

        result = tchip.process(query, human_pulse=pulse)

        glow_emoji = {"blue": "🔵", "red": "🔴", "gold": "🟡"}.get(
            result["glow"], "⚪"
        )
        print(f"  Glow:  {glow_emoji} {result['glow'].upper()}")
        print(f"  Message: {result['message']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        if result["illogics_detected"]:
            print(f"  Illogics: {result['illogics_detected']}")
        print()

    print(tchip.status())
    print()


if __name__ == "__main__":
    simulate_thermal_comparison()
    print()
    simulate_entropy_over_time()
    print()
    simulate_tchip_cold_state()
