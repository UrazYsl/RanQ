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
    if value > MAX_BITS:
        raise ValueError(f"Value cannot be larger than max bits: {MAX_BITS}")
    return value


def str_validation(attribute: str) -> str:
    if attribute == "":
        raise ValueError("Atrribute name must not be empty")
    return attribute


# No entanglement and other fancy stuff yet
class QInput(BaseModel):
    groups: dict[
        Annotated[str, AfterValidator(str_validation)],
        Annotated[int, AfterValidator(int_validation)],
    ]


# Basic health check
@app.get("/")
def read_root():
    return {"status": "ok"}


# Request bit generation
@app.post("/quantum/bits")
async def generate(qinput: QInput):
    return {
        "bits": active_provider.generate_qubits(qinput.groups),
        "backend": active_provider.name,
    }
