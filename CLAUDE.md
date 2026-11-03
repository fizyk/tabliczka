# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python 3.15 is pinned in `mise.toml`; dependencies are managed with `uv`.

```sh
uv run pytest                                # all tests
uv run pytest tests/test_practice.py::<name> # one test
uv run tabliczka --imie <name> dodawanie     # run the CLI
python main.py                               # same, asking for name and drill
prek run --all-files                         # formatters, linters, ty
uv run --group windows pyinstaller --onefile --console --name tabliczka \
  src/tabliczka/__main__.py                  # the Windows program, built on Windows
```

Every pull request adds a towncrier newsfragment,
`newsfragments/<issue>.<type>.rst`, with a type from `[tool.towncrier]` in
`pyproject.toml`. Releases are cut by the scheduled release workflow with tbump;
never bump the version by hand.

## Architecture

A Click CLI that drills children on arithmetic until they type `koniec` or press
Ctrl+C, then prints a score summary. User-facing text is Polish.

Each domain subpackage has `api.py`, `service.py` and `models/` with one class per
file. `api.py` holds the functions other packages call, and each calls the
services; it does not re-export them. Across packages, import `api` functions and
`models` types only.

- `exercises` - one class per operation (`Add`, `Subtract`, `Multiply`, `Divide`)
  in `service.py`, satisfying the `Operation` protocol, kept as singletons in
  `OPERATIONS_BY_ID`. Each builds a `Question` whose largest number, at most
  `max_n`, is the operation's own choice (the sum, the minuend, each factor), and
  has its own `default_max_n`. It holds no Polish text: a question carries only its
  `expression`, such as `2+4`. `get_operations(operation_ids)` in `api.py` looks
  them up.
- `practice` - `Drill(operation_ids, max_n=, question_count=)` in `api.py` holds
  the operations, limits and `Scoreboard`; `drill.questions()` yields its
  questions, `drill.check_answer(question, given)` scores each and
  `drill.summary()` returns the `Summary` of scores, through the stateless functions
  in `service.py`. It knows nothing of the terminal and never
  decides which operations run.
- `__main__.py` - the entry point PyInstaller packages; as the Windows program it
  waits for a key before its console window closes.
- `ui/cli.py` - the group takes `--imie` and asks for a missing name or drill; each
  subcommand only picks the operation ids and passes `--max` and `--pytania` on.
  `run_drill` owns the terminal: the prompt loop, the stop word, the feedback and
  the printed summary, all through the `practice` API. All the Polish copy lives
  here, including each operation's heading in `OPERATION_HEADINGS_BY_ID`.

New drills (printable worksheets and others; see the GitHub issues) should pass
different operations or arguments to `Drill`, not add new question logic; a new
user interface writes only its own loop over `questions()` and `check_answer()`.
The design rationale is in `.junie/plans/modularise-tabliczka-cli.md`.

Pushing a `v*` tag runs `.github/workflows/windows-release.yml`, which builds
`tabliczka.exe` on Windows and publishes it in a GitHub Release with that version's
`CHANGES.rst` section.

## Glossary

`docs/glossary.md` holds the domain vocabulary. Harvest it from these surfaces, in
this order:

1. The domain types `Question` and `Operation` in `exercises/models/`.
2. The operation ids, default largest numbers and singletons in
   `exercises/service.py`.
3. `Drill` in `practice/api.py`, and `Score`, `Scoreboard` and `Summary` in
   `practice/models/`.
4. The Polish interface copy: commands, options, prompts, help text, headings and
   the summary in `ui/cli.py`.

## Published text

- Interface copy, read by the child: `click.echo`, `click.prompt` and `click.pause`
  text, the feedback, the summary and `OPERATION_HEADINGS_BY_ID` in `ui/cli.py` and
  `__main__.py`.
- Validation messages, read by the child: `self.fail(...)` in `LearnerAnswer`.
- Validation messages, read by the parent: `click.BadParameter` in `ui/cli.py`.
- Option and command help, read by the parent: `help=` in `ui/cli.py`.
- Exception messages, read by the developer: `raise` in `exercises/` and
  `practice/`.
- Release notes, read by the parent: `newsfragments/*.rst`, built into
  `CHANGES.rst` and each GitHub Release.

## Preserved behaviour

These are deliberate; do not "fix" them without being asked:

- Subtraction asks `(x+y)-x` and division `(x*y):x`, so answers stay positive
  integers within the largest number.
