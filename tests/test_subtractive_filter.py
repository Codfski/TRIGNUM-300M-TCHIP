import pytest

from trignum_core.subtractive_filter import SubtractiveFilter


def test_subtractive_filter_initialization():
    filter_instance = SubtractiveFilter()
    assert filter_instance is not None
    assert hasattr(filter_instance, "UNIVERSAL_ILLOGICS")
    assert len(filter_instance.UNIVERSAL_ILLOGICS) > 0
    assert len(filter_instance._history) == 0


def test_filter_finds_contradiction():
    filter_instance = SubtractiveFilter()
    text = "The sky is blue but at the same time the sky is never blue."
    result = filter_instance.apply(text)

    assert result.has_illogics() is True
    assert "contradict" in result.illogics_found[0].lower()
    assert result.confidence > 0.5


def test_filter_passes_factual_statement():
    filter_instance = SubtractiveFilter()
    text = "Paris is the capital of France and water boils at 100 degrees Celsius."
    result = filter_instance.apply(text)

    assert result.has_illogics() is False
    assert len(result.illogics_found) == 0
    assert result.subtraction_ratio == 0.0


def test_filter_dict_processing():
    filter_instance = SubtractiveFilter()
    data = {
        "statement_1": "Everything I say is a lie.",
        "statement_2": "The previous statement is true.",
    }
    result = filter_instance.apply(data)

    # Simple recursive string check in dictionaries
    assert result.has_illogics() is True
