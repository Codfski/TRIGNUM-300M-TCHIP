"""
The Trignum Pyramid: Core geometric structure.

The pyramid is a tetrahedron with three magnetic faces (α, β, γ) and an apex
where the Trignomed Tensor collapses into Sovereign Reality.
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from .faces import FaceAlpha, FaceBeta, FaceGamma
from .magnetic_field import MagneticField


class PyramidState(Enum):
    """States of the Trignum Pyramid."""
    IDLE = "idle"
    SEPARATING = "separating"
    VACUUM_FORMING = "vacuum_forming"
    COLLAPSING = "collapsing"
    SOVEREIGN = "sovereign"
    FROZEN = "frozen"


@dataclass
class TrignumOutput:
    """The output of a Trignum Pyramid processing cycle."""
    result: Any
    logic_component: float
    illogic_component: float
    context_component: float
    state: PyramidState
    confidence: float
    freeze_coordinates: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TrignumPyramid:
    """
    The Trignum Pyramid: A tetrahedron with three magnetic faces.

    Face α (Alpha, Logic)   — Attracts coherent patterns (+)
    Face β (Beta, Illogic)  — Attracts contradictions (−), creates vacuum
    Face γ (Gamma, Context) — Attracts human sovereignty (~)

    The Apex is where the three streams reconnect into a Trignomed Tensor.
    """

    def __init__(
        self,
        logic_strength: float = 1.0,
        illogic_strength: float = 1.0,
        context_strength: float = 1.0,
        freeze_threshold: float = 0.7,
    ):
        """
        Initialize the Trignum Pyramid.

        Args:
            logic_strength: Magnetic strength of Face α (0.0 to 2.0)
            illogic_strength: Magnetic strength of Face β (0.0 to 2.0)
            context_strength: Magnetic strength of Face γ (0.0 to 2.0)
            freeze_threshold: Illogic ratio that triggers THE FREEZE (0.0 to 1.0)
        """
        self.face_alpha = FaceAlpha(strength=logic_strength)
        self.face_beta = FaceBeta(strength=illogic_strength)
        self.face_gamma = FaceGamma(strength=context_strength)
        self.magnetic_field = MagneticField(
            self.face_alpha, self.face_beta, self.face_gamma
        )
        self.freeze_threshold = freeze_threshold
        self.state = PyramidState.IDLE
        self._history: List[TrignumOutput] = []

    def process(
        self,
        data: Any,
        human_pulse: Optional[float] = None,
    ) -> TrignumOutput:
        """
        Process data through Magnetic Trillage.

        The data enters as undifferentiated Ferro-Data and is separated
        by the tri-polar magnetic field into Logic, Illogic, and Context
        components.

        Args:
            data: Input data (Ferro-Data) to process.
            human_pulse: Optional human sovereignty signal (0.0 to 1.0).
                         If None, the system may FREEZE at boundary.

        Returns:
            TrignumOutput with the processed result.
        """
        self.state = PyramidState.SEPARATING

        # Phase 1: Injection — data enters as Ferro-Data
        ferro_data = self._inject(data)

        # Phase 2: Magnetic Separation — data self-orients
        logic_pull = self.face_alpha.attract(ferro_data)
        illogic_pull = self.face_beta.attract(ferro_data)
        context_pull = self.face_gamma.attract(ferro_data)

        total_pull = logic_pull + illogic_pull + context_pull
        if total_pull == 0:
            total_pull = 1e-10  # Avoid division by zero

        logic_ratio = logic_pull / total_pull
        illogic_ratio = illogic_pull / total_pull
        context_ratio = context_pull / total_pull

        # Phase 3: Check for THE FREEZE
        if illogic_ratio >= self.freeze_threshold:
            self.state = PyramidState.FROZEN
            freeze_coords = self._compute_freeze_coordinates(
                logic_ratio, illogic_ratio, context_ratio
            )
            output = TrignumOutput(
                result=None,
                logic_component=logic_ratio,
                illogic_component=illogic_ratio,
                context_component=context_ratio,
                state=PyramidState.FROZEN,
                confidence=0.0,
                freeze_coordinates=freeze_coords,
                metadata={
                    "message": "🔴 T-CHIP FROZEN. Illogic boundary detected. "
                               "Human Pulse required.",
                    "illogic_ratio": illogic_ratio,
                    "threshold": self.freeze_threshold,
                },
            )
            self._history.append(output)
            return output

        # Phase 4: Vacuum Formation
        self.state = PyramidState.VACUUM_FORMING
        vacuum_strength = self.face_beta.create_vacuum(illogic_ratio)

        # Phase 5: Apply Human Pulse (if provided)
        if human_pulse is not None:
            context_ratio *= human_pulse
            self.face_gamma.apply_pulse(human_pulse)

        # Phase 6: Collapse at Apex — Magnetic Reconnection
        self.state = PyramidState.COLLAPSING
        result = self._collapse_at_apex(
            ferro_data, logic_ratio, illogic_ratio, context_ratio,
            vacuum_strength
        )

        # Compute confidence
        confidence = self._compute_confidence(
            logic_ratio, illogic_ratio, context_ratio, human_pulse
        )

        # Determine final state
        if human_pulse is not None and human_pulse > 0.5:
            self.state = PyramidState.SOVEREIGN
        else:
            self.state = PyramidState.IDLE

        output = TrignumOutput(
            result=result,
            logic_component=logic_ratio,
            illogic_component=illogic_ratio,
            context_component=context_ratio,
            state=self.state,
            confidence=confidence,
            metadata={
                "vacuum_strength": vacuum_strength,
                "human_pulse": human_pulse,
            },
        )
        self._history.append(output)
        return output

    def _inject(self, data: Any) -> Dict[str, Any]:
        """Convert raw data into Ferro-Data for magnetic processing."""
        if isinstance(data, str):
            return {
                "raw": data,
                "tokens": data.split(),
                "length": len(data),
                "entropy": self._estimate_entropy(data),
            }
        elif isinstance(data, (int, float)):
            return {
                "raw": data,
                "tokens": [str(data)],
                "length": 1,
                "entropy": 0.0,
            }
        elif isinstance(data, dict):
            return {
                "raw": data,
                "tokens": list(data.keys()),
                "length": len(data),
                "entropy": self._estimate_entropy(str(data)),
            }
        else:
            return {
                "raw": data,
                "tokens": [str(data)],
                "length": 1,
                "entropy": 0.5,
            }

    def _estimate_entropy(self, text: str) -> float:
        """Estimate Shannon entropy of text as proxy for information density."""
        if not text:
            return 0.0
        freq: Dict[str, int] = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        length = len(text)
        entropy = 0.0
        for count in freq.values():
            p = count / length
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def _compute_freeze_coordinates(
        self, logic: float, illogic: float, context: float
    ) -> List[float]:
        """Compute the Semantic Boundary Coordinates of a Freeze event."""
        return [logic, illogic, context]

    def _collapse_at_apex(
        self,
        ferro_data: Dict[str, Any],
        logic_ratio: float,
        illogic_ratio: float,
        context_ratio: float,
        vacuum_strength: float,
    ) -> Any:
        """
        Perform Magnetic Reconnection at the Apex.

        The three streams reconnect in a single point, producing
        the Trignomed Tensor — the output.
        """
        # The result is the raw data, weighted by the dominant face
        result = {
            "trignomed_tensor": ferro_data["raw"],
            "dominant_face": (
                "α (Logic)" if logic_ratio >= max(illogic_ratio, context_ratio)
                else "β (Illogic)" if illogic_ratio >= context_ratio
                else "γ (Context)"
            ),
            "vacuum_applied": vacuum_strength > 0,
            "face_weights": {
                "alpha": round(logic_ratio, 4),
                "beta": round(illogic_ratio, 4),
                "gamma": round(context_ratio, 4),
            },
        }
        return result

    def _compute_confidence(
        self,
        logic: float,
        illogic: float,
        context: float,
        pulse: Optional[float],
    ) -> float:
        """
        Compute confidence score for the output.

        High confidence when:
        - Logic is dominant
        - Illogic is low (well-filtered)
        - Context is present (Human Pulse applied)
        """
        base = logic * (1 - illogic)
        if pulse is not None:
            base *= (0.5 + 0.5 * pulse)
        return min(max(base, 0.0), 1.0)

    @property
    def history(self) -> List[TrignumOutput]:
        """Return processing history."""
        return self._history.copy()

    def reset(self) -> None:
        """Reset pyramid to IDLE state and clear history."""
        self.state = PyramidState.IDLE
        self._history.clear()
        self.face_alpha.reset()
        self.face_beta.reset()
        self.face_gamma.reset()

    def __repr__(self) -> str:
        return (
            f"TrignumPyramid(state={self.state.value}, "
            f"faces=[α={self.face_alpha.strength:.2f}, "
            f"β={self.face_beta.strength:.2f}, "
            f"γ={self.face_gamma.strength:.2f}])"
        )
