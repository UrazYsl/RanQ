from fastapi import FastAPI
from pydantic import BaseModel
from random import randint
app = FastAPI()

#No entanglement and other fancy stuff yet
class QInput(BaseModel):
    groups: dict[str, int]

#Basic health check
@app.get("/")
def read_root():
    return {"status": "ok"}

#Basic endpoint to request fake classical generation
@app.post("/quantum/bits")
async def generate(qinput: QInput):
    return {"bits": classical_generation(qinput), "backend": "classical"}

def classical_generation(qinput: QInput):
    ret = ""
    ret_dict = {}

    for attribute in qinput.groups:
        for _ in range(qinput.groups[attribute]):
            ret += str(randint(0, 1))
        ret_dict[attribute] = ret
        ret = ""
    return ret_dict