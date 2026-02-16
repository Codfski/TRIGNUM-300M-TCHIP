"""
Magnetic Field: The tri-polar field that drives Magnetic Trillage.

Data moves along field lines without resistance — achieving
computational superconductivity.
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class FieldVector:
    """A magnetic field vector in Trignum space."""
    alpha: float   # Logic component
    beta: float    # Illogic component
    gamma: float   # Context component

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.alpha**2 + self.beta**2 + self.gamma**2)

    @property
    def normalized(self) -> "FieldVector":
        mag = self.magnitude
        if mag == 0:
            return FieldVector(0, 0, 0)
        return FieldVector(self.alpha / mag, self.beta / mag, self.gamma / mag)

    @property
    def dominant_face(self) -> str:
        vals = {"α (Logic)": self.alpha, "β (Illogic)": self.beta, "γ (Context)": self.gamma}
        return max(vals, key=vals.get)

    def __repr__(self) -> str:
        return f"FieldVector(α={self.alpha:.3f}, β={self.beta:.3f}, γ={self.gamma:.3f})"


class MagneticField:
    """
    The tri-polar magnetic field of the Trignum Pyramid.

    Creates the field that drives Magnetic Trillage — data separates
    by self-orienting along field lines rather than being pushed
    through computational stages.
    """

    def __init__(self, face_alpha, face_beta, face_gamma):
        """
        Initialize the Magnetic Field from three faces.

        Args:
            face_alpha: The Logic pole (positive charge).
            face_beta: The Illogic pole (negative charge / vacuum).
            face_gamma: The Context pole (resonant frequency).
        """
        self.face_alpha = face_alpha
        self.face_beta = face_beta
        self.face_gamma = face_gamma
        self._field_lines: List[FieldVector] = []
        self._energy: float = 0.0

    def compute_field(self, position: Tuple[float, float, float]) -> FieldVector:
        """
        Compute the field vector at a given position in Trignum space.

        Position is a 3D coordinate (x, y, z) where:
        - x-axis: Logic dimension
        - y-axis: Illogic dimension
        - z-axis: Context dimension

        Returns:
            FieldVector at the given position.
        """
        x, y, z = position

        # Face α pulls toward (1, 0, 0)
        alpha_pull = self.face_alpha.strength / max(
            math.sqrt((x - 1)**2 + y**2 + z**2), 0.01
        )

        # Face β pulls toward (0, 1, 0) — negative charge creates vacuum
        beta_pull = -self.face_beta.strength / max(
            math.sqrt(x**2 + (y - 1)**2 + z**2), 0.01
        )

        # Face γ pulls toward (0, 0, 1) — resonant frequency
        gamma_pull = self.face_gamma.strength / max(
            math.sqrt(x**2 + y**2 + (z - 1)**2), 0.01
        )

        vector = FieldVector(alpha_pull, abs(beta_pull), gamma_pull)
        self._field_lines.append(vector)
        return vector

    def compute_apex(self) -> FieldVector:
        """
        Compute the field vector at the Apex of the pyramid.

        The Apex is the point of Magnetic Reconnection where
        all three streams converge.
        """
        # Apex is equidistant from all three faces
        apex_pos = (1/3, 1/3, 1/3)
        return self.compute_field(apex_pos)

    def get_trillage_path(
        self,
        start: Tuple[float, float, float],
        steps: int = 100,
        step_size: float = 0.01,
    ) -> List[Tuple[float, float, float]]:
        """
        Compute the path a Ferro-Data particle would take through the field.

        Args:
            start: Starting position in Trignum space.
            steps: Number of simulation steps.
            step_size: Size of each step.

        Returns:
            List of positions along the path.
        """
        path = [start]
        pos = list(start)

        for _ in range(steps):
            field = self.compute_field(tuple(pos))
            normalized = field.normalized

            # Move along field lines
            pos[0] += normalized.alpha * step_size
            pos[1] += normalized.beta * step_size
            pos[2] += normalized.gamma * step_size

            # Clamp to valid space
            pos = [max(0, min(1, p)) for p in pos]
            path.append(tuple(pos))

        return path

    @property
    def total_energy(self) -> float:
        """Total energy in the magnetic field (should approach zero in Cold State)."""
        if not self._field_lines:
            return 0.0
        return sum(v.magnitude for v in self._field_lines) / len(self._field_lines)

    def reset(self) -> None:
        """Reset field lines and energy."""
        self._field_lines.clear()
        self._energy = 0.0

    def __repr__(self) -> str:
        return (
            f"MagneticField(lines={len(self._field_lines)}, "
            f"energy={self.total_energy:.4f})"
        )
