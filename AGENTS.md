# AGENTS.md

Guidance for coding agents working on **borreguil**.

## Project mission

borreguil is a Python Web3/Ethereum JSON-RPC library focused on **performance**, **minimalism**, and a small, explicit API surface. Prefer simple, direct implementations over web3.py-style abstraction layers unless compatibility is intentionally required.

Primary goals:

- Fast JSON-RPC calls with low overhead.
- Minimal dependencies and no unnecessary framework code.
- Clear, typed Python APIs for common EVM operations.
- Small, maintainable ABI encoding/decoding utilities.
- Compatibility only where it supports the project goals or the documented replacement spec.

See `web3spec.md` for the broader web3.py replacement inventory and `docs/docs/*.md` for user-facing documentation.

## Repository layout

- `src/borreguil/provider.py` — HTTP JSON-RPC provider and direct `eth_*` helpers.
- `src/borreguil/contract.py` — contract abstraction and function-call builder.
- `src/borreguil/types/provider.py` — provider-facing data structures and filter builders.
- `src/borreguil/utils/abi_encoding.py` — lightweight ABI/function-call encoding.
- `src/borreguil/utils/blocks.py` — block identifier validation/parsing.
- `src/borreguil/utils/crypto.py` — Keccak hashing.
- `src/borreguil/errors.py` — project exception hierarchy.
- `examples/` — runnable examples.
- `docs/` — Docusaurus documentation site.

## Development commands

This project uses `uv`.

```bash
uv sync
uv run ruff check .
uv run ruff format .
uv run ty check
```

If tests are added or changed, run the relevant test command with `uv run`.

## Code style

- Python target: **3.11+**.
- Use modern Python typing syntax (`str | None`, `list[str]`, etc.).
- Keep functions small, explicit, and allocation-conscious.
- Use `orjson` for JSON deserialization in hot RPC paths.
- Avoid adding dependencies unless there is a strong performance or correctness reason.
- Prefer dataclasses or small typed structures over dynamic wrappers.
- Keep public APIs stable and documented when changing behavior.
- Follow Ruff formatting: double quotes, 120-character line length.

## Performance and minimalism rules

- Do not introduce middleware stacks, dynamic plugin systems, broad compatibility shims, or global registries unless explicitly requested.
- Avoid copying web3.py internals wholesale. Implement only the behavior this library needs.
- Prefer direct JSON-RPC method wrappers over deeply nested abstractions.
- Be careful with per-call allocations in provider and ABI code.
- Validate inputs at API boundaries, but avoid excessive defensive layers in internal hot paths.

## Ethereum/RPC conventions

- JSON-RPC requests must use `jsonrpc: "2.0"`, a monotonically increasing `id`, a `method`, and a `params` list.
- RPC hex quantities should be parsed with `int(value, 16)` and emitted with `hex(value)` where required.
- Block identifiers should go through `parse_block_identifier()`.
- Keep accepted special block tags aligned with EVM JSON-RPC: `latest`, `earliest`, `pending`, `safe`, `finalized`.
- Use checksum-address typing (`ChecksumAddress`) where appropriate, but avoid runtime conversions unless the API requires them.

## ABI and contracts

- `Contract.functions.<name>(*args).call()` currently returns the raw JSON-RPC response. If adding ABI decoding, do it deliberately and update docs/examples.
- ABI encoding utilities should remain lightweight. Add support incrementally with focused tests for each Solidity type.
- Function selectors are Keccak-256 of the ASCII signature, first 4 bytes.
- Dynamic ABI data must follow standard head/tail offset encoding.

## Error handling

- Raise project-specific exceptions from `src/errors.py` for public API failures.
- Preserve useful RPC error details: code, message, and optional data.
- Wrap malformed JSON responses in `DeserializationFailed`.
- Avoid raising bare `Exception`; add a small explicit exception type if needed.

## Testing guidance

- Prefer deterministic unit tests for ABI encoding, block parsing, filter construction, and RPC response handling.
- Avoid tests that depend on public RPC endpoints unless they are explicitly marked/invoked as integration tests.
- Mock `httpx.Client` or provider responses for normal unit tests.

## Documentation

When changing user-visible behavior, update:

- `README.md` if the quick project overview changes.
- `docs/docs/*.md` for user-facing usage changes.
- `examples/` when examples no longer match the API.

## Before committing changes

- Run `uv run ruff check .` and `uv run ruff format .`.
- Run type checking with `uv run ty check` when touching typed APIs.
- Ensure changes keep the library small, fast, and explicit.
