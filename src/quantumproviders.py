from random import randint


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
            for i in range(groups.get(attribute)):
                bitstr += str(randint(0, 1))
            bits[attribute] = bitstr
            bitstr = ""
        return bits
