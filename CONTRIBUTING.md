# Contributing to RanQ

Thanks for your interest. RanQ is in early development, so the design is still moving. Check `docs/roadmap.md` and the open issues before starting larger work, and open an issue first to discuss anything that changes the API (`docs/api_contract.md`).

## Reporting bugs and requesting features

Use the bug report or feature request template. For bugs, say which backend you used (classical, simulator or IBM Quantum) and include the request you sent and the response you got.

## Development setup

RanQ uses [uv](https://docs.astral.sh/uv/) and Python 3.11 or newer.

```bash
git clone https://github.com/UrazYsl/RanQ.git
cd RanQ
uv sync --all-extras
```

The classical and simulator backends need no credentials. For the IBM Quantum backend, copy `.env.example` to `.env` and fill in your API token and instance CRN. Never commit `.env`.

## Checks

CI runs these on Python 3.11 and 3.12. Run them before opening a pull request:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov --cov-fail-under=80
```

## Pull requests

- Branch from `main` and keep each pull request focused on one change.
- Add tests for new behavior; coverage must stay at 80% or above.
- Link the issue the pull request addresses.
- Keep game logic out of the service: RanQ returns raw bits, and the game decides what they mean.

## License

By contributing, you agree that your contributions are licensed under the MIT License of this project.
