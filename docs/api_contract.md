# RanQ API Contract

The contract between Godot (the game) and the RanQ quantum service. The service provides raw quantum random bits. It knows nothing about what the bits mean; the game decides how to interpret them.

## Endpoint

```
POST /quantum/bits
```

## Request

```json
{ "groups": [3, 2, 3] }
```

`groups` is a list of group sizes. Each number is how many bits that group needs. The example above asks for three groups of 3, 2, and 3 bits (8 bits total).

## Response

```json
{ "bits": ["011", "01", "001"], "backend": "simulator" }
```

`bits` is a list of bit strings, one per requested group, in the same order as the request. Each is a string of "0" and "1" characters of the requested length.

`backend` names the provider that produced the bits (`classical`, `simulator`, or `ibm`). Used for logging and the research comparison.

## Rules

- The total bits requested (the sum of `groups`) is capped at 1000. The cap is set in server config and can be changed.
- The backend is chosen server-side via config. The caller never specifies it.
- Bits are always returned as strings of "0" and "1".
- Groups are returned in the same order they were requested.
- The caller interprets the bits. The service has no knowledge of attributes, enemies, items, or anything game-specific.

## Usage example

To generate an enemy with three single-bit attributes (wings, armored, ranged) and one two-bit attribute (size), the game sends:

```json
{ "groups": [1, 1, 1, 2] }
```

and reads the response chunks in order: chunk 0 is wings, chunk 1 is armored, chunk 2 is ranged, chunk 3 is size (read as a 2-bit value). The mapping from bits to meaning lives entirely in the game.