#!/usr/bin/env python3
"""
Magnetic Trillage Simulation

Visualizes how Ferro-Data particles move through the tri-polar
magnetic field, self-separating into Logic, Illogic, and Context.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from trignum_core import TrignumPyramid, MagneticField
from trignum_core.magnetic_field import FieldVector


def simulate_particle_paths(n_particles: int = 10):
    """
    Simulate multiple Ferro-Data particles moving through the field.

    Each particle starts at a random position and follows field lines
    to its destination face.
    """
    import random

    pyramid = TrignumPyramid()
    field = pyramid.magnetic_field

    print("=" * 60)
    print("🧲 MAGNETIC TRILLAGE SIMULATION")
    print("=" * 60)
    print(f"\nSimulating {n_particles} Ferro-Data particles...")
    print()

    destinations = {"α (Logic)": 0, "β (Illogic)": 0, "γ (Context)": 0}

    for i in range(n_particles):
        # Random starting position in Trignum space
        start = (
            random.uniform(0.1, 0.9),
            random.uniform(0.1, 0.9),
            random.uniform(0.1, 0.9),
        )

        # Compute path through field
        path = field.get_trillage_path(start, steps=50, step_size=0.02)

        # Determine final destination
        final = path[-1]
        final_field = field.compute_field(final)
        dest = final_field.dominant_face

        destinations[dest] += 1

        print(f"  Particle {i+1:2d}: Start({start[0]:.2f}, {start[1]:.2f}, {start[2]:.2f}) "
              f"→ {dest} (steps: {len(path)})")

    print()
    print("─" * 40)
    print("SEPARATION RESULTS:")
    print("─" * 40)
    for face, count in destinations.items():
        bar = "█" * (count * 3)
        print(f"  {face:15s}: {count:3d} {bar}")

    print()
    print(f"  Field Energy: {field.total_energy:.4f}")
    print(f"  Field Lines:  {len(field._field_lines)}")
    print()

    return destinations


def simulate_vacuum_formation():
    """
    Simulate the Magnetic Vacuum forming at Face β.

    Shows how Illogic creates a vacuum that pulls Truth toward it.
    """
    pyramid = TrignumPyramid()

    print("=" * 60)
    print("🕳️  VACUUM FORMATION SIMULATION")
    print("=" * 60)
    print()

    # Process data with increasing Illogic content
    test_data = [
        "The sky is blue and water is wet",                          # Low illogic
        "The sky is always blue but never blue at night",           # Medium illogic
        "Everything is true and everything is false always never",  # High illogic
    ]

    for data in test_data:
        result = pyramid.process(data)
        print(f"  Input:   \"{data[:50]}...\"")
        print(f"  Logic:   {result.logic_component:.3f}")
        print(f"  Illogic: {result.illogic_component:.3f}")
        print(f"  Context: {result.context_component:.3f}")
        print(f"  State:   {result.state.value}")
        if result.state.value == "frozen":
            print(f"  ❄️  FREEZE COORDINATES: {result.freeze_coordinates}")
        print()

    pyramid.reset()


if __name__ == "__main__":
    simulate_particle_paths(15)
    print("\n" + "=" * 60 + "\n")
    simulate_vacuum_formation()
