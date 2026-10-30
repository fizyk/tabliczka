# Glossary

Polish terms are what the learner sees; identifiers are English.

## Drill

| Term | Definition | Canonical identifier | Where defined |
|---|---|---|---|
| drill (ćwiczenie) | A run of randomly chosen questions that lasts until the learner types the stop word or presses Ctrl+C. | `run_drill` | `src/tabliczka/session.py`, `run_drill` |
| operation | An arithmetic skill a drill can ask questions about. | `Operation` | `src/tabliczka/operations.py`, `Operation` |
| operation id | The fixed name that identifies an operation in the scores. | `id`; values `add`, `subtract`, `multiplication`, `division` | `src/tabliczka/operations.py`, `Operation.id` |
| addition (Dodawanie) | The operation that asks for the sum of two operands. | `ADD`, class `Add` | `src/tabliczka/operations.py`, `Add` |
| subtraction (Odejmowanie) | The operation that asks `(x+y)-x`, so the answer is the operand `y`. | `SUBTRACT`, class `Subtract` | `src/tabliczka/operations.py`, `Subtract` |
| multiplication (Mnożenie) | The operation that asks for the product of two operands. | `MULTIPLY`, class `Multiply` | `src/tabliczka/operations.py`, `Multiply` |
| division (Dzielenie) | The operation that asks `(x*y):x`, so the answer is the operand `y`. | `DIVIDE`, class `Divide` | `src/tabliczka/operations.py`, `Divide` |
| question | One exercise put to the learner, with its expected answer. | `Question` | `src/tabliczka/operations.py`, `Question` |
| prompt | The text of a question as shown to the learner. | `prompt` | `src/tabliczka/operations.py`, `Question.prompt` |
| answer | The correct result of a question. | `answer` | `src/tabliczka/operations.py`, `Question.answer` |
| learner answer | What the learner types in reply to a question: a whole number or the stop word. | `LearnerAnswer` | `src/tabliczka/session.py`, `LearnerAnswer` |
| stop word (koniec) | The word that ends a drill when typed instead of an answer. | `STOP_WORD` | `src/tabliczka/session.py`, `STOP_WORD` |
| operand range | The lowest and highest operand a question may use, 1 to 10 by default. | `min_n`, `max_n` | `src/tabliczka/operations.py`, `Operation.generate` |

## Scoring

| Term | Definition | Canonical identifier | Where defined |
|---|---|---|---|
| scoreboard | The record of a drill's results, printed when the drill ends. | `Scoreboard` | `src/tabliczka/session.py`, `Scoreboard` |
| score | The counts of correct and wrong answers for one operation. | `scores[operation_id]` | `src/tabliczka/session.py`, `Scoreboard.scores` |
| correct count (dobrze) | The number of questions answered correctly. | `ok` | `src/tabliczka/session.py`, `Scoreboard.record` |
| wrong count (źle) | The number of questions answered wrongly. | `bad` | `src/tabliczka/session.py`, `Scoreboard.record` |
| total | The correct and wrong counts summed over all operations in a drill. | `ok`, `bad` | `src/tabliczka/session.py`, `Scoreboard.print_summary` |
| heading | The title of one operation's section in the score summary. | `heading` | `src/tabliczka/operations.py`, `Operation.heading` |

## Command line

| Term | Definition | Canonical identifier | Where defined |
|---|---|---|---|
| learner name (imię ucznia) | The name the program greets the learner by. | `name`; `--imie` on the command line | `src/tabliczka/cli.py`, `main` |
| addition drill (dodawanie) | The command that drills addition and subtraction. | `dodawanie` | `src/tabliczka/cli.py`, `dodawanie` |
| multiplication drill (mnozenie) | The command that drills multiplication and division. | `mnozenie` | `src/tabliczka/cli.py`, `mnozenie` |

## Spelled two ways

- **Operation names.** Classes and singletons use verbs for every operation (`Add`,
  `Subtract`, `Multiply`, `Divide`), but operation ids mix verbs and nouns (`add`,
  `subtract`, `multiplication`, `division`).
- **Learner name.** The command line option is `--imie`; the code holds it as `name`.
- **Multiplication drill.** The command is `mnozenie` (no Polish letters); the copy
  says `Mnożenie`.
- **Correct and wrong.** `run_drill` holds the outcome as `correct`; the scoreboard
  stores it under `ok` and `bad`.

## One word, two meanings

- **answer.** `Question.answer` is the correct result; the local `answer` in
  `run_drill` is what the learner typed.
- **`ok` and `bad`.** Keys of one operation's score in `Scoreboard.scores`; locals
  holding the totals in `Scoreboard.print_summary`.
