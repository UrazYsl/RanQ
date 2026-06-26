# RanQ #
RanQ is an open source Godot extension meant to use the true randomness of quantum measurement for procedural generation. It uses Qiskit to interact with the quantum computer(or simulation) and a FastAPI
interface for Godot.

Basic Pipeline:
Quantum Service <-> Qiskit <-> FastAPI <-> Godot

# Components #
## Quantum Computer/Simulator ##
This part of the extension is where the true randomness happens. By either simulating or connecting to a quantum computer, we are able to measure the state of its qubits for the procedural generation.

## Qiskit ##
Qiskit helps us build and run the circuits for quantum computers so that we can get a meaningful output.

## FastAPI ##
FastAPI is the middle layer that receives requests, decides which backend, and returns results. Sets up the communications between Qiskit and Godot.

## Godot ##
Godot is an open source game engine which the extension will be based off of. It will request procedural generation through FastAPI. Godot won't know a quantum backend exists, it will just request for generation.

# Connections #
## Godot to FastAPI ##
Godot requests procedural generation through FastAPI which then runs the Qiskit circuits for result.

## FastAPI to Qiskit ##
FastAPI delivers the requests to Qiskit's quantum circuits, and the reverse.
Both live in the same service as both are Python based.

## Qiskit to Quantum Computer/Simulator ##
Qiskit authenticates with an API token and instance CRN, picks a backend (a real machine or a simulator), transpiles the circuit so it matches that specific hardware's layout, submits it as a job, and because real hardware has a queue, waits for the result before returning it.


# Design Choices #
## Provider Abstraction ##
As a design choice, we decided that instead of just connecting to a quantum computer or running on simulation, the extension will be a swappable interface with classical, simulator, and real hardware implementations behind it.

This lets us test and develop without any quantum hardware since the classical and simulator backends run locally for free, and it makes the research comparison easy because switching from classical to quantum is just a config change rather than a rewrite.

## REST as The Bridge ##
Godot and the quantum service talk over REST (HTTP/JSON on localhost), which is enough because generation happens at discrete moments, not every frame.

## Building a Plugin Rather Than an Engine ##
As a small team, we do not have the manpower nor the time to develop and test a game engine. Instead of writing one, we will use Godot, which is open source. In addition, we only plan to integrate quantum computers/simulators for generation. So writing a whole engine just to test procedural generation does not make sense.

## Separating Godot From The Quantum Service ##
Separated Godot from the quantum service as both are independent processes in two different languages. The benefit is that neither depends on the other's internals, which allows us to be more flexible. We can rewrite either of the two, or both and the other wouldn't be affected as long as REST contract is untouched.