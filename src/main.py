from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator
from typing import Annotated

from config import MAX_BITS, BACKEND
from quantumproviders import ClassicalProvider, SimulatorProvider

app = FastAPI()
providers = {
    "classical": ClassicalProvider(),
    "simulator": SimulatorProvider(),
}
active_provider = providers[BACKEND]


def int_validation(value: int) -> int:
    if value < 0:
        raise ValueError("Value must be larger or equal to 0")
    return value


def str_validation(attribute: str) -> str:
    if attribute == "":
        raise ValueError("Attribute name must not be empty")
    return attribute

def dict_validation(groups: dict[str, int]) -> dict:
    totl = sum(groups.values())
    if totl > MAX_BITS:
        raise ValueError(f"Total value cannot be larger than max bits: {MAX_BITS}")
    return groups

# No entanglement and other fancy stuff yet
# Dict validates separately for max bit count, int checks for negative values.
class QInput(BaseModel):
    groups: Annotated[
        dict[
            Annotated[str, AfterValidator(str_validation)],
            Annotated[int, AfterValidator(int_validation)],
        ],
        AfterValidator(dict_validation),
    ]


# Basic health check
@app.get("/")
def read_root():
    return {"status": "ok"}


# Request bit generation
# Not using async because I want the generation to run in external thread pool, otherwise a slow call would block the event loop
# A known issue to fix later is the timeout in godot, if the hardware takes too long. Commented on issue #39.
@app.post("/quantum/bits")
def generate(qinput: QInput):
    return {
        "bits": active_provider.generate_qubits(qinput.groups),
        "backend": active_provider.name,
    }
