# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python 3.15 is pinned in `mise.toml`; dependencies are managed with `uv`.

```sh
uv run pytest                                # all tests
uv run pytest tests/test_practice.py::<name> # one test
uv run tabliczka --imie <name> dodawanie     # run the CLI
python main.py                               # same, asking for name and drill
uv run python -m tabliczka                   # the window
prek run --all-files                         # formatters, linters, ty
uv run --group windows pyinstaller --onefile --windowed --name tabliczka \
  src/tabliczka/__main__.py                  # the Windows program, built on Windows
```

Every pull request adds a towncrier newsfragment,
`newsfragments/<issue>.<type>.rst`, with a type from `[tool.towncrier]` in
`pyproject.toml`. Releases are cut by the scheduled release workflow with tbump;
never bump the version by hand.

## Architecture

A PySide6 window, and a Click CLI for running from source, that drill children on
arithmetic until they stop, then show a score summary. User-facing text is Polish.

Each domain subpackage has `api.py`, `service.py` and `models/` with one class per
file. `api.py` holds the functions other packages call, and each calls the
services; it does not re-export them. Across packages, import `api` functions,
`models` types and `core` constants only.

- `core/constants.py` - constants the whole program shares, such as
  `APPLICATION_NAME`.
- `exercises` - one class per operation (`Add`, `Subtract`, `Multiply`, `Divide`)
  in `service.py`, satisfying the `Operation` protocol, kept as singletons in
  `OPERATIONS_BY_ID`. Each builds a `Question` whose largest number, at most
  `largest_number`, is the operation's own choice (the sum, the minuend, each
  factor), and has its own `default_largest_number` and the smallest
  `largest_number` it accepts, `smallest_largest_number`. It holds no Polish text:
  a question carries only its `expression`, such as `2+4`.
  `get_operations(operation_ids)` in `api.py` looks them up.
- `practice` - `Drill(operation_ids, largest_number=, question_count=)` in `api.py`
  holds the operations, limits and `Scoreboard`; `drill.questions()` yields its
  questions, `drill.check_answer(question, given)` scores each and
  `drill.summary()` returns the `Summary` of scores, through the stateless functions
  in `service.py`. It knows nothing of the terminal and never
  decides which operations run.
- `profiles` - `load_profile()` and `save_profile(profile)` in `api.py` keep one
  `Profile` per user account: the learner's name, operation ids, `largest_number` and
  `question_count`. `load_profile()` returns an empty profile, with no name and
  no operations, when none is saved. `service.py` finds the file in the account's
  app data folder with `platformdirs` and rejects one it cannot read back;
  `ProfileRepository` in `repository.py` reads and writes it as JSON.
- `__main__.py` - the entry point PyInstaller packages; it opens the window.
- `ui/text.py` - the Polish copy both interfaces show: each operation's heading in
  `OPERATION_HEADINGS_BY_ID`, the greeting, the question, the feedback and the
  summary lines.
- `ui/cli.py` - the group takes `--imie` and asks for a missing name or drill; each
  subcommand only picks the operation ids and passes `--max` and `--pytania` on.
  `run_drill` owns the terminal: the prompt loop, the stop word, the feedback and
  the printed summary, all through the `practice` API. Its own Polish copy, the
  commands, options and prompts, lives here.
- `ui/gui/` - the window, one thing per module. `pages/start.py`, `pages/question.py`
  and `pages/summary.py` hold one page each: `StartPage` returns the name and the
  drill as one `Profile` and is built from one, `QuestionPage` asks one question
  at a time and reports each answer with its `answered` signal, and `SummaryPage`
  shows the summary. `drill_window.py` holds `DrillWindow`, which builds the start
  page from the loaded profile, saves it again at each start, moves between the
  pages and shows the feedback; pages never touch each other's widgets.
  `rich_text.py` colours the feedback and the summary, `text.py` holds the
  window's own Polish copy, and `application.py` holds `main`, which shows any
  unexpected error in a message.

New drills (printable worksheets and others; see the GitHub issues) should pass
different operations or arguments to `Drill`, not add new question logic; a new
user interface writes only its own loop over `questions()` and `check_answer()`.
The design rationale is in `.junie/plans/modularise-tabliczka-cli.md`.

Pushing a `v*` tag runs `.github/workflows/windows-release.yml`, which builds
the windowed `tabliczka.exe` on Windows and publishes it in a GitHub Release with that version's
`CHANGES.rst` section.

## Glossary

`docs/glossary.md` holds the domain vocabulary. Harvest it from these surfaces, in
this order:

1. The domain types `Question` and `Operation` in `exercises/models/`.
2. The operation ids, default largest numbers and singletons in
   `exercises/service.py`.
3. `Drill` in `practice/api.py`, and `Score`, `Scoreboard` and `Summary` in
   `practice/models/`.
4. `Profile` in `profiles/models/`.
5. The Polish interface copy: headings, feedback and the summary in `ui/text.py`;
   commands, options, prompts and help text in `ui/cli.py`; labels and buttons in
   `ui/gui/text.py`.

## Published text

- Interface copy, read by the child: everything in `ui/text.py` and
  `ui/gui/text.py`; `click.echo` and `click.prompt` text in `ui/cli.py`.
- Validation messages, read by the child: `self.fail(...)` in `LearnerAnswer`.
- Validation messages, read by the parent: `click.BadParameter` in `ui/cli.py`.
- Option and command help, read by the parent: `help=` in `ui/cli.py`.
- Exception messages, read by the developer: `raise` in `exercises/`,
  `practice/` and `profiles/`.
- Release notes, read by the parent: `newsfragments/*.rst`, built into
  `CHANGES.rst` and each GitHub Release.

## Preserved behaviour

These are deliberate; do not "fix" them without being asked:

- Subtraction asks `(x+y)-x` and division `(x*y):x`, so answers stay positive
  integers within the largest number.
