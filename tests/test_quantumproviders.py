import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from quantumproviders import ClassicalProvider


def test_name_is_classical():
    provider = ClassicalProvider()
    assert provider.name == "classical"


def test_generate_qubits_returns_correct_keys():
    provider = ClassicalProvider()
    result = provider.generate_qubits({"a": 3, "b": 5})
    assert set(result.keys()) == {"a", "b"}


def test_generate_qubits_returns_correct_lengths():
    provider = ClassicalProvider()
    result = provider.generate_qubits({"a": 3, "b": 5})
    assert len(result["a"]) == 3
    assert len(result["b"]) == 5


def test_generate_qubits_only_zeros_and_ones():
    provider = ClassicalProvider()
    result = provider.generate_qubits({"a": 50})
    assert set(result["a"]) <= {"0", "1"}


def test_generate_qubits_empty_input():
    provider = ClassicalProvider()
    result = provider.generate_qubits({})
    assert result == {}


def test_generate_qubits_zero_count():
    provider = ClassicalProvider()
    result = provider.generate_qubits({"a": 0})
    assert result["a"] == ""


def test_generate_qubits_negative_count_currently_returns_empty():
    """KNOWN GAP: range() with a negative stop is silently empty in
    Python, so this doesn't raise — it just returns "". Flagging in
    case ClassicalProvider itself should reject negative counts rather
    than relying on API-layer validation (which also doesn't enforce
    this currently — see test_main.py)."""
    provider = ClassicalProvider()
    result = provider.generate_qubits({"a": -3})
    assert result["a"] == ""


def test_generate_qubits_independent_calls_dont_share_state():
    """Regression guard: an earlier version of this loop reused a
    `bitstr` accumulator across attributes. Confirms each group's
    bits are independent and not leaking into the next group."""
    provider = ClassicalProvider()
    result = provider.generate_qubits({"a": 3, "b": 4})
    assert len(result["a"]) == 3
    assert len(result["b"]) == 4
