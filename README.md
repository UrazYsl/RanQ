# RanQ

True quantum randomness for Godot. Procedural generation powered by qubits.

RanQ is an open source Godot extension that provides genuinely random bits from quantum measurement. Most games use pseudorandom number generators, which are deterministic: given the same seed, they always produce the same result. RanQ instead measures real qubits (or a simulation of them), so the randomness is physically non-deterministic. The service hands back raw bits, and your game decides what they mean.

## How it works

```
Quantum Service <-> Qiskit <-> FastAPI <-> Godot
```

A small Python service measures qubits and exposes the bits over a local REST API. Godot requests bits when it needs them (on a room load, a floor transition, an item drop) and runs its own logic to turn those bits into game content. The service knows nothing about your game; it only provides randomness.

## Backends

RanQ uses a swappable backend, chosen by server config:

- **Classical** uses Python's random. No setup, runs locally, useful as a baseline.
- **Simulator** runs real quantum circuits locally via Qiskit Aer.
- **IBM Quantum** runs on real quantum hardware over the cloud.

The same game code works against all three. Switching is a config change, not a rewrite.

## Why raw bits

RanQ returns raw bits rather than finished game content like enemies or items. This keeps it general: the service has no idea what a "wing" or an "enemy" is, so any game can use it, not just a roguelike. Your game reads the bits and decides what they represent, which keeps all the game logic in the game where it belongs.

## Status

RanQ is in early development. See `docs/` for the design:

- `docs/architecture.md` for how the pieces fit together
- `docs/roadmap.md` for the build plan
- `docs/api_contract.md` for the exact request and response shapes

## License

MIT