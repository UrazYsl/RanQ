# RanQ API Contract

The contract between Godot (the game) and the RanQ quantum service. The service provides raw quantum random bits. It knows nothing about what the bits mean; the game decides how to interpret them.

## Endpoint

```
POST /quantum/bits
```

## Request

```json
{ "groups": { "attr1": 3, "attr2": 2, "attr3": 3 } }```

`groups` is a list of group sizes. Each key is a name of an attribute you choose, and its value is how many bits that group needs.
The names are just labels for you to to identify each group, which the service won't know.
The example above asks for three groups: attr1 (3 bits), attr2 (2 bits), and attr3 (3 bits), for 8 bits total.

## Response

```json
{ "bits": { "attr1": "011", "attr2": "01", "attr3": "001" }, "backend": "simulator" }
```

`bits` returns one bit string per requested group, under the same name. Each is a string of "0" and "1" of the requested length.
`backend` names the provider that produced the bits (`classical`, `simulator`, or `ibm`). Used for logging and the research comparison.

## Rules

- Total bits requested (sum of `groups` values) is capped at 1000. Set in server config, changeable.
- Backend is chosen server-side via config. The caller never specifies it.
- Bits are always returned as strings of "0" and "1".
- Each requested group name appears in the response under the same name. Groups are independent, so a problem with one does not shift or affect the others.
- The caller interprets the bits. The service knows nothing game-specific.

## Usage example

To generate an enemy with three single-bit attributes (wings, armored, ranged) and one two-bit attribute (size), the game sends:

```json
{ "groups": { "wings": 1, "armored": 1, "ranged": 1, "size": 2 } }
```

and reads the response chunks in order: chunk 0 is wings, chunk 1 is armored, chunk 2 is ranged, chunk 3 is size (read as a 2-bit value). The mapping from bits to meaning lives entirely in the game.