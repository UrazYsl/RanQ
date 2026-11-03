import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
import quantumproviders
from config import CIRCUIT_WIDTH
from quantumproviders import ClassicalProvider, SimulatorProvider, IBMProvider

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


# IBM tests never contact IBM: QiskitRuntimeService is replaced with a fake,
# and the credentials are patched on the module, so no .env is needed.
class FakeService:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.least_busy_kwargs = None

    def least_busy(self, **kwargs):
        self.least_busy_kwargs = kwargs
        return "fake_backend"


@pytest.fixture
def ibm_env(monkeypatch):
    monkeypatch.setattr(quantumproviders, "QiskitRuntimeService", FakeService)
    monkeypatch.setattr(quantumproviders, "IBM_TOKEN", "fake-token")
    monkeypatch.setattr(quantumproviders, "IBM_CRN", "fake-crn")
    return monkeypatch


def test_name_is_ibm(ibm_env):
    assert IBMProvider().name == "ibm"


def test_ibm_logs_in_with_credentials(ibm_env):
    provider = IBMProvider()
    assert provider.service.kwargs == {
        "channel": "ibm_quantum_platform",
        "token": "fake-token",
        "instance": "fake-crn",
    }


def test_ibm_selects_least_busy_backend_wide_enough(ibm_env):
    provider = IBMProvider()
    assert provider.service.least_busy_kwargs == {"min_num_qubits": CIRCUIT_WIDTH}
    assert provider.backend == "fake_backend"


@pytest.mark.parametrize("variable", ["IBM_TOKEN", "IBM_CRN"])
@pytest.mark.parametrize("value", [None, ""])
def test_ibm_missing_or_empty_credential_rejected(ibm_env, variable, value):
    ibm_env.setattr(quantumproviders, variable, value)
    with pytest.raises(ValueError, match=variable):
        IBMProvider()


def test_ibm_does_not_log_in_without_credentials(ibm_env):
    """The checks must run before the login, so an empty token is
    never sent to IBM."""

    def fail(**kwargs):
        raise AssertionError("tried to log in")

    ibm_env.setattr(quantumproviders, "QiskitRuntimeService", fail)
    ibm_env.setattr(quantumproviders, "IBM_TOKEN", "")
    with pytest.raises(ValueError):
        IBMProvider()
