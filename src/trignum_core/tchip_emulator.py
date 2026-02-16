"""
T-CHIP Emulator: The Tensor Character (v.300M)

"He does not think. He reflects. When you see him freeze—red and silent—
he is waiting for you to be Sovereign."

T-CHIP = Trignomed Centrifuge & Human Interface Particle
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .pyramid import TrignumPyramid, PyramidState
from .subtractive_filter import SubtractiveFilter


class TCHIPGlow(Enum):
    """T-CHIP glow states — visual indicators of processing state."""
    OFF = "off"           # Not active
    BLUE = "blue"         # Logic Stable (Processing)
    RED = "red"           # Illogic Detected (THE FREEZE)
    GOLD = "gold"         # Human Pulse Locked (Sovereign Reality)


class TCHIPVibration(Enum):
    """T-CHIP vibration patterns."""
    STILL = "still"           # At rest (off or frozen)
    STEADY = "steady"         # Rhythmic pulse (logic processing)
    RESONANT = "resonant"     # Synchronizing with Human Pulse
    TRILOCATION = "trilocation"  # All three faces active simultaneously


@dataclass
class TCHIPState:
    """Complete state snapshot of T-CHIP."""
    glow: TCHIPGlow
    vibration: TCHIPVibration
    message: str
    freeze_count: int = 0
    sovereign_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class TCHIP:
    """
    T-CHIP: The Tensor Character (v.300M)

    A dual-pyramid octahedron that sits at the center of the Trignum Pyramid.
    He does not think—he reflects. He does not know—he waits.

    Glow States:
        🔵 Blue  = Logic Stable (Processing)
        🔴 Red   = Illogic Detected (THE FREEZE)
        🟡 Gold  = Human Pulse Locked (Sovereign Reality)
    """

    VERSION = "v.300M"

    def __init__(
        self,
        pyramid: Optional[TrignumPyramid] = None,
        freeze_threshold: float = 0.7,
    ):
        """
        Initialize T-CHIP.

        Args:
            pyramid: Optional TrignumPyramid instance. If None, creates default.
            freeze_threshold: Illogic ratio that triggers THE FREEZE.
        """
        self.pyramid = pyramid or TrignumPyramid(
            freeze_threshold=freeze_threshold
        )
        self.subtractive_filter = SubtractiveFilter()
        self._glow = TCHIPGlow.OFF
        self._vibration = TCHIPVibration.STILL
        self._freeze_count = 0
        self._sovereign_count = 0
        self._history: List[TCHIPState] = []
        self._born = time.time()

    @property
    def state(self) -> str:
        """Current glow state as string."""
        return self._glow.value.upper()

    @property
    def glow(self) -> TCHIPGlow:
        """Current glow color."""
        return self._glow

    @property
    def vibration(self) -> TCHIPVibration:
        """Current vibration pattern."""
        return self._vibration

    def process(
        self,
        data: Any,
        human_pulse: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Process data through T-CHIP.

        T-CHIP wraps the Trignum Pyramid with:
        - Glow state management
        - The Subtractive Snap
        - Human interface

        Args:
            data: Input data to process.
            human_pulse: Optional human sovereignty signal (0.0 to 1.0).

        Returns:
            Dict with processed result, glow state, and metadata.
        """
        # Phase 1: Pre-filter through Subtractive Filter
        self._glow = TCHIPGlow.BLUE
        self._vibration = TCHIPVibration.STEADY
        filter_result = self.subtractive_filter.apply(data)

        # Phase 2: Process through Trignum Pyramid
        pyramid_output = self.pyramid.process(
            data=filter_result.truth_remaining,
            human_pulse=human_pulse,
        )

        # Phase 3: Update T-CHIP state based on pyramid output
        if pyramid_output.state == PyramidState.FROZEN:
            self._glow = TCHIPGlow.RED
            self._vibration = TCHIPVibration.STILL
            self._freeze_count += 1
            message = (
                "🔴 T-CHIP FROZEN. Illogic boundary detected at coordinates "
                f"{pyramid_output.freeze_coordinates}. "
                "Human Pulse required to proceed."
            )
        elif pyramid_output.state == PyramidState.SOVEREIGN:
            self._glow = TCHIPGlow.GOLD
            self._vibration = TCHIPVibration.RESONANT
            self._sovereign_count += 1
            message = (
                "🟡 SOVEREIGN REALITY ACHIEVED. "
                f"Confidence: {pyramid_output.confidence:.2%}. "
                "The Truth has collapsed at the Apex."
            )
        else:
            self._glow = TCHIPGlow.BLUE
            self._vibration = TCHIPVibration.STEADY
            message = (
                "🔵 Processing complete. "
                f"Confidence: {pyramid_output.confidence:.2%}."
            )

        # Record state
        state = TCHIPState(
            glow=self._glow,
            vibration=self._vibration,
            message=message,
            freeze_count=self._freeze_count,
            sovereign_count=self._sovereign_count,
            metadata={
                "filter_illogics": filter_result.illogics_found,
                "pyramid_state": pyramid_output.state.value,
                "confidence": pyramid_output.confidence,
            },
        )
        self._history.append(state)

        return {
            "result": pyramid_output.result,
            "glow": self._glow.value,
            "vibration": self._vibration.value,
            "message": message,
            "confidence": pyramid_output.confidence,
            "illogics_detected": filter_result.illogics_found,
            "face_weights": {
                "logic": pyramid_output.logic_component,
                "illogic": pyramid_output.illogic_component,
                "context": pyramid_output.context_component,
            },
        }

    def subtractive_snap(self, data: Any) -> Dict[str, Any]:
        """
        Perform The Subtractive Snap.

        T-CHIP's signature move: rapid rotation on vertical axis,
        creating a Magnetic Vacuum that pulls all noise into Face β.

        Result: Noise In, 💎 Out.

        Args:
            data: Noisy input data.

        Returns:
            Dict with the single Truth remaining after snap.
        """
        # Phase 1: Detection
        self._glow = TCHIPGlow.BLUE
        self._vibration = TCHIPVibration.TRILOCATION

        # Phase 2: Spin — apply Subtractive Filter aggressively
        filter_result = self.subtractive_filter.apply(data)

        # Phase 3: Suction — all noise pulled into Face β
        if filter_result.illogics_found:
            self._glow = TCHIPGlow.RED
            self._vibration = TCHIPVibration.STILL

        # Phase 4: Snap — return to rest with single Truth
        self._glow = TCHIPGlow.BLUE
        self._vibration = TCHIPVibration.STEADY

        return {
            "💎": filter_result.truth_remaining,
            "noise_removed": filter_result.illogics_removed,
            "subtraction_ratio": filter_result.subtraction_ratio,
            "snap_complete": True,
        }

    def provide_pulse(self, pulse: float = 1.0) -> Dict[str, Any]:
        """
        Provide the Human Pulse to unfreeze T-CHIP.

        Args:
            pulse: Sovereignty signal strength (0.0 to 1.0).

        Returns:
            Dict with the post-pulse state.
        """
        if self._glow != TCHIPGlow.RED:
            return {
                "message": "T-CHIP is not frozen. No Pulse needed.",
                "glow": self._glow.value,
            }

        # Apply Pulse to the Context face
        self.pyramid.face_gamma.apply_pulse(pulse)

        if pulse >= 0.5:
            self._glow = TCHIPGlow.GOLD
            self._vibration = TCHIPVibration.RESONANT
            self._sovereign_count += 1
            return {
                "message": "🟡 SOVEREIGN REALITY ACHIEVED. T-CHIP unfrozen.",
                "glow": self._glow.value,
                "pulse_strength": pulse,
            }
        else:
            self._glow = TCHIPGlow.BLUE
            self._vibration = TCHIPVibration.STEADY
            return {
                "message": "🔵 T-CHIP unfrozen. Processing resumed.",
                "glow": self._glow.value,
                "pulse_strength": pulse,
            }

    @property
    def history(self) -> List[TCHIPState]:
        """Return T-CHIP state history."""
        return self._history.copy()

    @property
    def age(self) -> float:
        """Time since T-CHIP was born (seconds)."""
        return time.time() - self._born

    def status(self) -> str:
        """Get a formatted status string."""
        return (
            f"╔═══════════════════════════════════════╗\n"
            f"║  T-CHIP [{self.VERSION}]               ║\n"
            f"╠═══════════════════════════════════════╣\n"
            f"║  Glow:      {self._glow.value.upper():>10}             ║\n"
            f"║  Vibration: {self._vibration.value:>10}             ║\n"
            f"║  Freezes:   {self._freeze_count:>10}             ║\n"
            f"║  Sovereigns:{self._sovereign_count:>10}             ║\n"
            f"║  Age:       {self.age:>8.1f}s             ║\n"
            f"╚═══════════════════════════════════════╝"
        )

    def reset(self) -> None:
        """Reset T-CHIP to initial state."""
        self._glow = TCHIPGlow.OFF
        self._vibration = TCHIPVibration.STILL
        self._freeze_count = 0
        self._sovereign_count = 0
        self._history.clear()
        self.pyramid.reset()
        self.subtractive_filter.reset()

    def __repr__(self) -> str:
        return f"TCHIP(glow={self._glow.value}, vibration={self._vibration.value})"
