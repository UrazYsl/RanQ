# RanQ #
RanQ is an open source Godot extension that provides the true randomness of quantum measurement for procedural generation. It uses Qiskit to interact with the quantum computer (or simulation) and a FastAPI interface for Godot. The service provides raw random bits; the game decides what they mean.

Basic Pipeline:
Quantum Service <-> Qiskit <-> FastAPI <-> Godot

# Components #
## Quantum Computer/Simulator ##
This part of the extension is where the true randomness happens. By either simulating or connecting to a quantum computer, we measure the state of its qubits to produce raw random bits.

## Qiskit ##
Qiskit helps us build and run the circuits for quantum computers so that we can get the measured bits back.

## FastAPI ##
FastAPI is the middle layer that receives bit requests, selects the backend based on server config, and returns the raw bits. It sets up the communication between Qiskit and Godot.

## Godot ##
Godot is an open source game engine which the extension is based on. It requests raw bits from the service and runs its own generation logic on them, deciding what each bit means. Godot won't know a quantum backend exists, it just asks for bits.

# Connections #
## Godot to FastAPI ##
Godot requests raw bits through FastAPI, which runs the Qiskit circuit and returns them. Godot then does all the generation on its side.

## FastAPI to Qiskit ##
FastAPI delivers the requests to Qiskit's quantum circuits, and the reverse. Both live in the same service as both are Python based.

## Qiskit to Quantum Computer/Simulator ##
Qiskit authenticates with an API token and instance CRN, picks a backend (a real machine or a simulator), transpiles the circuit so it matches that specific hardware's layout, submits it as a job, and because real hardware has a queue, waits for the result before returning it.

# Design Choices #
## Raw Bits, Not Game Content ##
The service returns raw quantum bits rather than finished game content like enemies or items. The game reads those bits and runs its own generation logic to decide what they mean.

This keeps RanQ general. The service knows nothing about wings, enemies, or any game-specific idea, so any game can use it, not just our roguelike. It also keeps the generation logic in the game where the game knowledge lives, and it is efficient since the service only ever measures qubits and hands back bits.

## Provider Abstraction ##
Instead of just connecting to a quantum computer or running on simulation, the extension is a swappable interface with classical, simulator, and real hardware implementations behind it.

This lets us test and develop without any quantum hardware since the classical and simulator backends run locally for free, and it makes the research comparison easy because switching from classical to quantum is just a config change rather than a rewrite.

## Server-Side Backend Selection ##
The caller never picks the backend. The active backend (classical, simulator, or real hardware) is chosen by server config. The game just asks for bits and does not know or care which backend served them.

Requests are also capped at a configurable limit set in server config, to prevent a single request from asking for an unreasonable amount of bits. The exact request and response shapes are defined in api_contract.md.

## REST as The Bridge ##
Godot and the quantum service talk over REST (HTTP/JSON on localhost), which is enough because generation happens at discrete moments, not every frame.

## Building a Plugin Rather Than an Engine ##
As a small team, we do not have the manpower nor the time to develop and test a game engine. Instead of writing one, we use Godot, which is open source. In addition, we only plan to integrate quantum computers/simulators for generation. So writing a whole engine just to test procedural generation does not make sense.

## Separating Godot From The Quantum Service ##
We separated Godot from the quantum service as both are independent processes in two different languages. The benefit is that neither depends on the other's internals, which allows us to be more flexible. We can rewrite either of the two, or both, and the other wouldn't be affected as long as the REST contract is untouched.