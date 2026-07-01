# RanQ Roadmap

## Phase 1: Classical Pipeline
Goal: the full system works end to end with no quantum at all.
Tasks:
  - [X] Set up basic FastAPI server that runs
  - [X] Define the QuantumProvider abstract base class
  - [X] Implement the LocalClassical provider (using Python's random)
  - [X] Implement bit generation in the classical provider
  - [X] Add the /quantum/bits endpoint (returns grouped raw bits)
  - [X] Define the API contract doc (the agreed JSON shapes)
  - [ ] Build the Godot HTTP bridge (RanQ.gd that calls the endpoint)
  - [ ] Build a basic demo scene (renders something from the returned data)
  - [ ] Add request validation to /quantum/bits
  - [ ] Set up CI (ruff + pytest on PRs) once there's code to test

## Phase 2: Quantum Simulator
Goal: generation runs on real quantum circuits locally via Qiskit Aer.
Tasks:
  - [ ] Add Qiskit and Qiskit Aer as dependencies
  - [ ] Implement the QiskitSimulator provider (same interface, Aer backend)
  - [ ] Write the bit-generation circuit (Hadamard + measure)
  - [ ] Map measurement results to the grouped bit-string format
  - [ ] Wire the simulator provider into the /quantum/bits endpoint
  - [ ] Verify simulator output matches the API contract (same JSON shape as classical)
  - [ ] Add tests for the circuit and the provider

## Phase 3: Real Hardware (free tier)
Goal: the same circuits run on real IBM quantum hardware via the free tier.
Tasks:
  - [ ] Set up free IBM Quantum account (API token + instance CRN)
  - [ ] Implement the IBMQuantum provider (authenticate, select backend)
  - [ ] Add circuit transpilation for the target hardware
  - [ ] Handle job submission and polling (account for long free-tier queues)
  - [ ] Run a small bit generation on real hardware
  - [ ] Keep the API token out of the repo (.env, gitignored)

## Phase 4: Research Layer
Goal: classical, simulator, and quantum outputs are logged and comparable.
Tasks:
  - [ ] Build a logging wrapper around providers (records every call + which backend)
  - [ ] Log generation outputs to a file or dataset (backend, result, timestamp)
  - [ ] Implement the classical baseline for comparison (Kami)
  - [ ] Run the same generation across all backends and collect the data
  - [ ] Analyze and compare output distributions (classical vs simulator vs hardware)
  - [ ] Write up the findings

## Phase 5: Presentable Game
Goal: the demo is a coherent, playable, presentable roguelike, not finished but demoable.
Tasks:
  - [ ] Core gameplay loop (move, fight, descend floors)
  - [ ] Render generated enemies and items meaningfully (attributes visibly matter)
  - [ ] Basic combat or interaction system
  - [ ] Floor progression using generated layouts
  - [ ] Minimal UI (health, inventory, current floor)
  - [ ] Visual polish pass (sprites, feedback, feel)
  - [ ] A short playable run from start to a few floors deep

## Future
Goal: deeper quantum use and richer generation beyond the core.
Tasks:
  - [ ] Entanglement for correlated attributes (related qubits influence each other)
  - [ ] Richer/correlated bit generation
  - [ ] D-Wave / QUBO for map layout (constraint-based dungeon generation)
  - [ ] Larger entangled circuits encoding more of the floor state