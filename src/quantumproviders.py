from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from random import randint
from math import ceil
from config import CIRCUIT_WIDTH, IBM_CRN, IBM_TOKEN


class QuantumProvider:
    name: str

    def __init__(self, name: str):
        self.name = name

    def generate_qubits(self, groups: dict[str, int]) -> dict[str, str]:
        raise NotImplementedError


class ClassicalProvider(QuantumProvider):
    def __init__(self):
        super().__init__("classical")

    def generate_qubits(self, groups: dict[str, int]) -> dict[str, str]:
        bits = {}
        bitstr = ""
        for attribute in groups:
            for _ in range(groups.get(attribute)):
                bitstr += str(randint(0, 1))
            bits[attribute] = bitstr
            bitstr = ""
        return bits


class SimulatorProvider(QuantumProvider):
    def __init__(self):
        super().__init__("simulator")

    def generate_qubits(self, groups: dict[str, int]) -> dict[str, str]:
        total_random = sum(groups.values())
        q_str = ""
        # When total bits are 0, get_memory() crashes
        if total_random > 0:
            # Hadamard Gate(h) puts each qubit into superposition
            # measure_all collapses them into bits
            qc = QuantumCircuit(CIRCUIT_WIDTH)
            for q in range(CIRCUIT_WIDTH):
                qc.h(q)
            qc.measure_all()
            sim = AerSimulator()
            # Run enough shots to cover the total, concatenate, then slice into groups
            shots = ceil(total_random / CIRCUIT_WIDTH)
            job = sim.run(qc, shots=shots, memory=True)
            result = job.result()
            memory = result.get_memory()
            for measurement in memory:
                q_str += measurement

        group_results = {}
        iteration = 0
        for key in groups.keys():
            group_results[key] = q_str[iteration : iteration + groups[key]]
            iteration += groups[key]

        return group_results


class IBMProvider(QuantumProvider):
    def __init__(self):
        super().__init__("ibm")
        if not IBM_TOKEN:
            raise ValueError("IBM_TOKEN is required in the .env for IBM Provider")
        if not IBM_CRN:
            raise ValueError("IBM_CRN is required in the .env for IBM Provider")
        self.service = QiskitRuntimeService(
            channel="ibm_quantum_platform", token=IBM_TOKEN, instance=IBM_CRN
        )
        # least_busy() already filters for online providers that aren't simulations.
        self.backend = self.service.least_busy(min_num_qubits=CIRCUIT_WIDTH)
