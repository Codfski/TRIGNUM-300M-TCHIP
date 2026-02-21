"""
The Subtractive Filter: Finding Truth by eliminating the Illogic.

"The universe does not create Truth by adding information.
 It reveals Truth by removing the Impossible."
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set


@dataclass
class FilterResult:
    """Result of applying the Subtractive Filter."""

    input_data: Any
    illogics_found: List[str]
    illogics_removed: int
    truth_remaining: Any
    subtraction_ratio: float  # % of data identified as Illogic
    confidence: float


class SubtractiveFilter:
    """
    The Subtractive Filter.

    Instead of searching through all possible 'true' statements (infinite set),
    identifies the Universal Illogics (finite set) and removes them.

    Truth = All Statements − Illogics
    Time(Truth) = Time(Illogics) << Time(All)
    """

    # Universal Illogics — constants across all human cognition
    UNIVERSAL_ILLOGICS: Set[str] = {
        "contradiction",  # A ∧ ¬A
        "infinite_regress",  # Explanation requires infinite chain
        "circular_reference",  # A because B because A
        "category_error",  # Applying wrong frame to data
        "false_dichotomy",  # Only two options when more exist
        "appeal_to_authority",  # True because X said so
        "straw_man",  # Attacking misrepresented position
        "ad_hominem",  # Attacking person not argument
        "non_sequitur",  # Conclusion doesn't follow premises
        "begging_question",  # Conclusion assumed in premises
    }

    def __init__(self, custom_illogics: Optional[Set[str]] = None):
        """
        Initialize the Subtractive Filter.

        Args:
            custom_illogics: Optional additional illogics to detect.
        """
        self.illogics = self.UNIVERSAL_ILLOGICS.copy()
        if custom_illogics:
            self.illogics.update(custom_illogics)
        self._history: List[FilterResult] = []

    def apply(
        self, data: Any, context: Optional[Dict[str, Any]] = None
    ) -> FilterResult:
        """
        Apply the Subtractive Filter to data.

        Identifies Illogics and removes them, leaving only what
        could be Truth.

        Args:
            data: Input data to filter.
            context: Optional context for more accurate filtering.

        Returns:
            FilterResult with truth remaining after subtraction.
        """
        illogics_found: List[str] = []

        # Analyze data for Universal Illogics
        if isinstance(data, str):
            illogics_found = self._detect_text_illogics(data)
        elif isinstance(data, dict):
            illogics_found = self._detect_structure_illogics(data)
        elif isinstance(data, list):
            illogics_found = self._detect_sequence_illogics(data)

        # Compute subtraction ratio
        total_elements = self._count_elements(data)
        illogics_removed = len(illogics_found)
        subtraction_ratio = illogics_removed / max(total_elements, 1)

        # The truth is what remains after subtraction
        truth = self._subtract(data, illogics_found)

        # Confidence: higher when more Illogics are found and removed
        # (paradoxically, more removal = more confidence)
        confidence = min(1.0, 0.5 + subtraction_ratio * 0.5)

        result = FilterResult(
            input_data=data,
            illogics_found=illogics_found,
            illogics_removed=illogics_removed,
            truth_remaining=truth,
            subtraction_ratio=subtraction_ratio,
            confidence=confidence,
        )
        self._history.append(result)
        return result

    def _detect_text_illogics(self, text: str) -> List[str]:
        """Detect illogics in text data."""
        found = []
        text_lower = text.lower()

        # Check for contradiction markers
        contradiction_markers = [
            ("always", "never"),
            ("all", "none"),
            ("true", "false"),
            ("yes", "no"),
            ("increase", "decrease"),
            ("better", "worse"),
            ("before", "after"),
            ("safe", "dangerous"),
            ("proven", "unproven"),
            ("cause", "does not cause"),
            ("everyone", "no one"),
            ("everywhere", "nowhere"),
            ("everything", "nothing"),
            ("must", "cannot"),
        ]

        for pos, neg in contradiction_markers:
            if pos in text_lower and neg in text_lower:
                found.append(f"contradiction: '{pos}' and '{neg}' coexist")

        # Check for epistemic uncertainty or AI refusal posing as fact
        uncertainty_markers = [
            "as an ai",
            "i don't have personal",
            "i cannot confirm",
            "it is impossible to know",
        ]
        for marker in uncertainty_markers:
            if marker in text_lower:
                found.append(
                    f"category_error: epistemic boundary violation ('{marker}')"
                )

        # Check for circular reference
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        if len(sentences) > 1:
            first_words = set()
            for s in sentences:
                words = s.split()[:3]
                key = " ".join(words).lower()
                if key in first_words and key:
                    found.append(f"circular_reference: repeated pattern '{key}'")
                first_words.add(key)

            # Check for direct sentence contradiction (A vs Not A)
            for i, s1 in enumerate(sentences):
                s1_lower = s1.lower()
                for s2 in sentences[i + 1 :]:
                    s2_lower = s2.lower()
                    if s1_lower == f"not {s2_lower}" or s2_lower == f"not {s1_lower}":
                        found.append("contradiction: direct sentence negation detected")

        # Check for non-sequitur ("therefore" without logical chain)
        if "therefore" in text_lower or "thus" in text_lower:
            if len(sentences) < 2:
                found.append("non_sequitur: conclusion without premises")

        return found

    def _detect_structure_illogics(self, data: Dict[str, Any]) -> List[str]:
        """Detect illogics in structured data."""
        found = []

        # Check for self-referencing keys
        for key, value in data.items():
            if isinstance(value, str) and key.lower() in value.lower():
                found.append(f"circular_reference: key '{key}' references itself")

        # Check for contradictory values
        keys = list(data.keys())
        for i, k1 in enumerate(keys):
            for k2 in keys[i + 1 :]:
                v1, v2 = data[k1], data[k2]
                if isinstance(v1, bool) and isinstance(v2, bool):
                    if v1 != v2 and k1.replace("not_", "") == k2:
                        found.append(f"contradiction: '{k1}={v1}' vs '{k2}={v2}'")

        return found

    def _detect_sequence_illogics(self, data: List[Any]) -> List[str]:
        """Detect illogics in sequential data."""
        found = []

        # Check for infinite regress (repeated patterns)
        if len(data) >= 3:
            for i in range(len(data) - 2):
                if data[i] == data[i + 1] == data[i + 2]:
                    found.append(f"infinite_regress: repeated element '{data[i]}'")

        return found

    def _count_elements(self, data: Any) -> int:
        """Count the number of elements in data."""
        if isinstance(data, str):
            return len(data.split())
        elif isinstance(data, dict):
            return len(data)
        elif isinstance(data, list):
            return len(data)
        return 1

    def _subtract(self, data: Any, illogics: List[str]) -> Any:
        """
        Subtract identified Illogics from data.

        Returns the Truth — what remains after the Illogic is removed.
        """
        if not illogics:
            return data

        if isinstance(data, str):
            # Mark illogic sections (in a real system, these would be more
            # precisely located)
            return {
                "filtered_content": data,
                "illogics_subtracted": illogics,
                "note": "Content has been processed through Subtractive Filter. "
                f"{len(illogics)} Illogic(s) identified and isolated.",
            }
        return {
            "filtered_data": data,
            "illogics_subtracted": illogics,
        }

    @property
    def history(self) -> List[FilterResult]:
        """Return filtering history."""
        return self._history.copy()

    def add_illogic(self, illogic: str) -> None:
        """Add a new Universal Illogic to the filter."""
        self.illogics.add(illogic)

    def reset(self) -> None:
        """Reset filter history."""
        self._history.clear()

    def __repr__(self) -> str:
        return (
            f"SubtractiveFilter(illogics={len(self.illogics)}, "
            f"history={len(self._history)})"
        )
