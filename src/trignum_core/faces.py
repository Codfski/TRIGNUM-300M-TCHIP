"""
The Three Faces of the Trignum Pyramid.

Face α (Alpha) — Logic Pole (Blue, Positive Charge)
Face β (Beta)  — Illogic Pole (Red, Negative Charge / Vacuum)
Face γ (Gamma) — Context / Human Pulse Pole (Gold, Resonant Frequency)
"""

import math
import random
from dataclasses import dataclass
from typing import Any, Dict, Optional


class FaceAlpha:
    """
    Face α — The Logic Pole (Blue).

    Attracts coherent patterns, statistical certainties, established knowledge.
    Magnetic charge: Positive.
    """

    COLOR = "blue"
    SYMBOL = "α"
    NAME = "Logic"

    def __init__(self, strength: float = 1.0):
        self.strength = max(0.0, min(2.0, strength))
        self._accumulated: float = 0.0
        self._cycles: int = 0

    def attract(self, ferro_data: Dict[str, Any]) -> float:
        """
        Calculate attraction strength for the given Ferro-Data.

        Logic attraction is proportional to:
        - Low entropy (structured, predictable data)
        - Token consistency
        - Pattern regularity
        """
        entropy = ferro_data.get("entropy", 0.5)
        length = ferro_data.get("length", 1)

        # Low entropy = high logic attraction
        attraction = self.strength * (1.0 - min(entropy / 8.0, 1.0))

        # Longer, structured data attracts more to Logic
        length_factor = min(math.log2(length + 1) / 10.0, 1.0)
        attraction *= (0.5 + 0.5 * length_factor)

        self._accumulated += attraction
        self._cycles += 1
        return attraction

    def reset(self) -> None:
        self._accumulated = 0.0
        self._cycles = 0

    def __repr__(self) -> str:
        return f"FaceAlpha(strength={self.strength:.2f}, cycles={self._cycles})"


class FaceBeta:
    """
    Face β — The Illogic Pole (Red).

    Attracts contradictions, anomalies, pulse-stopping impossibilities.
    Magnetic charge: Negative (creates vacuum).

    Does not process — it HALTS processing.
    """

    COLOR = "red"
    SYMBOL = "β"
    NAME = "Illogic"

    def __init__(self, strength: float = 1.0):
        self.strength = max(0.0, min(2.0, strength))
        self._accumulated: float = 0.0
        self._cycles: int = 0
        self._vacuum_active: bool = False

    def attract(self, ferro_data: Dict[str, Any]) -> float:
        """
        Calculate attraction strength for the given Ferro-Data.

        Illogic attraction is proportional to:
        - High entropy (chaotic, unpredictable data)
        - Contradictions
        - Anomalies in token patterns
        """
        entropy = ferro_data.get("entropy", 0.5)
        length = ferro_data.get("length", 1)

        # High entropy = high illogic attraction
        attraction = self.strength * min(entropy / 8.0, 1.0)

        # Add stochastic noise to simulate hallucination detection
        noise = random.gauss(0, 0.05)
        attraction = max(0.0, attraction + noise)

        self._accumulated += attraction
        self._cycles += 1
        return attraction

    def create_vacuum(self, illogic_ratio: float) -> float:
        """
        Create a Magnetic Vacuum based on accumulated Illogic.

        The vacuum is the key innovation — it pulls Truth by creating
        an absence of falsehood.

        Returns vacuum strength (0.0 to 1.0).
        """
        self._vacuum_active = True
        vacuum = illogic_ratio * self.strength
        return min(vacuum, 1.0)

    def reset(self) -> None:
        self._accumulated = 0.0
        self._cycles = 0
        self._vacuum_active = False

    @property
    def is_vacuum_active(self) -> bool:
        return self._vacuum_active

    def __repr__(self) -> str:
        return (
            f"FaceBeta(strength={self.strength:.2f}, "
            f"vacuum={'ON' if self._vacuum_active else 'OFF'})"
        )


class FaceGamma:
    """
    Face γ — The Context / Human Pulse Pole (Gold).

    Attracts the sovereign intent and emotional frequency of the human user.
    Magnetic charge: Resonant frequency.

    Collapses the wave-function when the Pulse is applied.
    """

    COLOR = "gold"
    SYMBOL = "γ"
    NAME = "Context"

    def __init__(self, strength: float = 1.0):
        self.strength = max(0.0, min(2.0, strength))
        self._accumulated: float = 0.0
        self._cycles: int = 0
        self._pulse_applied: bool = False
        self._pulse_value: float = 0.0

    def attract(self, ferro_data: Dict[str, Any]) -> float:
        """
        Calculate attraction strength for the given Ferro-Data.

        Context attraction is proportional to:
        - Presence of human-contextual markers
        - Emotional/intentional signals
        - Sovereignty indicators
        """
        entropy = ferro_data.get("entropy", 0.5)
        tokens = ferro_data.get("tokens", [])

        # Moderate entropy = highest context attraction (the sweet spot)
        mid_entropy = 1.0 - abs(entropy / 4.0 - 1.0)
        attraction = self.strength * max(0.0, mid_entropy)

        # Human-like token patterns increase attraction
        if tokens:
            # More diverse tokens suggest more human context
            unique_ratio = len(set(tokens)) / max(len(tokens), 1)
            attraction *= (0.5 + 0.5 * unique_ratio)

        self._accumulated += attraction
        self._cycles += 1
        return attraction

    def apply_pulse(self, pulse: float) -> None:
        """
        Apply the Human Pulse to the Context face.

        Args:
            pulse: Sovereignty signal strength (0.0 to 1.0).
                   1.0 = full sovereign presence
                   0.0 = no human engagement
        """
        self._pulse_applied = True
        self._pulse_value = max(0.0, min(1.0, pulse))

    def reset(self) -> None:
        self._accumulated = 0.0
        self._cycles = 0
        self._pulse_applied = False
        self._pulse_value = 0.0

    @property
    def is_pulse_active(self) -> bool:
        return self._pulse_applied

    @property
    def pulse_value(self) -> float:
        return self._pulse_value

    def __repr__(self) -> str:
        return (
            f"FaceGamma(strength={self.strength:.2f}, "
            f"pulse={'ON' if self._pulse_applied else 'OFF'}, "
            f"value={self._pulse_value:.2f})"
        )
