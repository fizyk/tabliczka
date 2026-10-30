# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python 3.15 is pinned in `mise.toml`; dependencies are managed with `uv`.

```sh
uv run pytest                                # all tests
uv run pytest tests/test_session.py::<name>  # one test
uv run tabliczka --imie <name> dodawanie     # run the CLI
python main.py                               # same, asking for name and drill
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
- `cli.py` - the group takes `--imie` and asks for a missing name or drill; each
  subcommand only picks the operation list.

New drills (mixed operations, a configurable maximum, printable worksheets; see
the GitHub issues) should pass different operations or arguments to `run_drill`,
not add new loops.
The design rationale is in `.junie/plans/modularise-tabliczka-cli.md`.

## Glossary

`docs/glossary.md` holds the domain vocabulary. Harvest it from these surfaces, in
this order:

1. The domain types `Question` and `Operation` in `operations.py`.
2. The operation ids and their singletons in `operations.py`.
3. The correct and wrong counts in `Scoreboard` in `session.py`.
4. The Polish interface copy: commands, prompts, help text, headings and the
   summary in `cli.py`, `operations.py` and `session.py`.

## Preserved behaviour

These are deliberate; do not "fix" them without being asked:

- Subtraction asks `(x+y)-x` and division `(x*y):x`, so answers stay positive
  integers within the operand range.
- In the summary, each operation's wrong-answer line is shown when the **total**
  wrong count is non-zero, not that operation's own count.
