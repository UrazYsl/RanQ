import os

MAX_BITS = 1000
CIRCUIT_WIDTH = 20
# "classical", "simulator", "ibm"
BACKEND = "simulator"
IBM_TOKEN = os.getenv("IBM_TOKEN")
IBM_CRN = os.getenv("IBM_CRN")
