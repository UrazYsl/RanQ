from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator, ValidationError
from typing import Annotated
from random import randint

from config import MAX_BITS
from quantumproviders import ClassicalProvider

classic = ClassicalProvider()
app = FastAPI()

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

#No entanglement and other fancy stuff yet
class QInput(BaseModel):
    groups: dict[Annotated[str, AfterValidator(str_validation)], Annotated[int, AfterValidator(int_validation)]]

#Basic health check
@app.get("/")
def read_root():
    return {"status": "ok"}


# Basic endpoint to request fake classical generation
@app.post("/quantum/bits")
async def generate(qinput: QInput):
    return {"bits": classic.generate_qubits(qinput.groups), "backend": classic.name}
