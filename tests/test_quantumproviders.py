import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
from quantumproviders import ClassicalProvider, SimulatorProvider

# Negative counts are rejected at the API layer (see int_validation in
# main.py), so providers assume clean input and are not tested for them.
# API-level rejection is tested in test_main.py.


# Name specific, can't parametrize neatly
def test_name_is_classical():
    provider = ClassicalProvider()
    assert provider.name == "classical"


# Name specific, can't parametrize neatly
def test_name_is_simulator():
    provider = SimulatorProvider()
    assert provider.name == "simulator"


@pytest.mark.parametrize("provider_class", [ClassicalProvider, SimulatorProvider])
def test_generate_qubits_returns_correct_keys(provider_class):
    provider = provider_class()
    result = provider.generate_qubits({"a": 3, "b": 5})
    assert set(result.keys()) == {"a", "b"}


@pytest.mark.parametrize("provider_class", [ClassicalProvider, SimulatorProvider])
def test_generate_qubits_returns_correct_lengths(provider_class):
    provider = provider_class()
    result = provider.generate_qubits({"a": 3, "b": 5})
    assert len(result["a"]) == 3
    assert len(result["b"]) == 5


@pytest.mark.parametrize("provider_class", [ClassicalProvider, SimulatorProvider])
def test_generate_qubits_only_zeros_and_ones(provider_class):
    provider = provider_class()
    result = provider.generate_qubits({"a": 50})
    assert set(result["a"]) <= {"0", "1"}


@pytest.mark.parametrize("provider_class", [ClassicalProvider, SimulatorProvider])
def test_generate_qubits_empty_input(provider_class):
    provider = provider_class()
    result = provider.generate_qubits({})
    assert result == {}


@pytest.mark.parametrize("provider_class", [ClassicalProvider, SimulatorProvider])
def test_generate_qubits_zero_count(provider_class):
    provider = provider_class()
    result = provider.generate_qubits({"a": 0})
    assert result["a"] == ""


@pytest.mark.parametrize("provider_class", [ClassicalProvider, SimulatorProvider])
def test_generate_qubits_negative_count_currently_returns_empty(provider_class):
    """KNOWN GAP: range() with a negative stop is silently empty in
    Python, so this doesn't raise, it just returns "". Flagging in
    case ClassicalProvider itself should reject negative counts rather
    than relying on API-layer validation."""
    provider = provider_class()
    result = provider.generate_qubits({"a": -3})
    assert result["a"] == ""


@pytest.mark.parametrize("provider_class", [ClassicalProvider, SimulatorProvider])
def test_generate_qubits_independent_calls_dont_share_state(provider_class):
    """Regression guard: an earlier version of this loop reused a
    `bitstr` accumulator across attributes. Confirms each group's
    bits are independent and not leaking into the next group."""
    provider = provider_class()
    result = provider.generate_qubits({"a": 3, "b": 4})
    assert len(result["a"]) == 3
    assert len(result["b"]) == 4


# No shots for classical
def test_simulator_handles_more_bits_than_circuit_width():
    provider = SimulatorProvider()
    result = provider.generate_qubits({"a": 50})
    assert len(result["a"]) == 50
