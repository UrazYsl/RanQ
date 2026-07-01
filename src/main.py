from fastapi import FastAPI
from pydantic import BaseModel

from quantumproviders import ClassicalProvider

classic = ClassicalProvider()
app = FastAPI()


# No entanglement and other fancy stuff yet
class QInput(BaseModel):
    groups: dict[str, int]


# Basic health check
@app.get("/")
def read_root():
    return {"status": "ok"}


# Basic endpoint to request fake classical generation
@app.post("/quantum/bits")
async def generate(qinput: QInput):
    return {"bits": classic.generate_qubits(qinput.groups), "backend": classic.name}
