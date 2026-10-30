# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python 3.15 is pinned in `mise.toml`; dependencies are managed with `uv`.

```sh
uv run pytest                                # all tests
uv run pytest tests/test_session.py::<name>  # one test
uv run tabliczka <name> dodawanie            # run the CLI
python main.py <name> mnozenie               # same, via the root shim
prek run --all-files                         # formatters, linters, ty
```

Every pull request adds a towncrier newsfragment,
`newsfragments/<issue>.<type>.rst`, with a type from `[tool.towncrier]` in
`pyproject.toml`. Releases are cut by the scheduled release workflow with tbump;
never bump the version by hand.

## Architecture

A Click CLI that drills children on arithmetic until Ctrl+C, then prints a score
summary. User-facing text is Polish.

- `operations.py` - one class per operation (`Add`, `Subtract`, `Multiply`,
  `Divide`) satisfying the `Operation` protocol, exported as singletons. Each
  builds a `Question` from operands in `[min_n, max_n]`.
- `session.py` - `run_drill(operations)` owns the loop, prompt, feedback and the
  `click.Abort` summary via `Scoreboard`. It never decides which operations run.
- `cli.py` - the group takes `name`; each subcommand only picks the operation list.

New drills (mixed operations, a configurable maximum, batch mode; see `TODO`)
should pass different operations or arguments to `run_drill`, not add new loops.
The design rationale is in `.junie/plans/modularise-tabliczka-cli.md`.

## Preserved behaviour

These are deliberate; do not "fix" them without being asked:

- Subtraction asks `(x+y)-x` and division `(x*y):x`, so answers stay positive
  integers within the operand range.
- In the summary, each operation's wrong-answer line is shown when the **total**
  wrong count is non-zero, not that operation's own count.
