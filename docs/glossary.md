# Glossary

Polish terms are what the learner sees; identifiers are English.

## Drill

| Term | Definition | Canonical identifier | Where defined |
|---|---|---|---|
| drill (ćwiczenie) | A run of randomly chosen questions that lasts until the learner types the stop word, presses Ctrl+C or has answered the number of questions. | `run_drill` | `src/tabliczka/practice/service.py`, `run_drill` |
| operation | An arithmetic skill a drill can ask questions about. | `Operation` | `src/tabliczka/exercises/models/operation.py`, `Operation` |
| operation id | The fixed name that identifies an operation in the scores. | `id`; values `add`, `subtract`, `multiplication`, `division` | `src/tabliczka/exercises/models/operation.py`, `Operation.id` |
| addition (Dodawanie) | The operation that asks for the sum of two operands, the sum at most the largest number. | `ADD`, class `Add` | `src/tabliczka/exercises/service.py`, `Add` |
| subtraction (Odejmowanie) | The operation that asks `(x+y)-x`, so the answer is the operand `y`, with the minuend `x+y` at most the largest number. | `SUBTRACT`, class `Subtract` | `src/tabliczka/exercises/service.py`, `Subtract` |
| multiplication (Mnożenie) | The operation that asks for the product of two operands, each at most the largest number. | `MULTIPLY`, class `Multiply` | `src/tabliczka/exercises/service.py`, `Multiply` |
| division (Dzielenie) | The operation that asks `(x*y):x`, so the answer is the operand `y`, with `x` and `y` at most the largest number. | `DIVIDE`, class `Divide` | `src/tabliczka/exercises/service.py`, `Divide` |
| operand | One of the two numbers a question is built from; in multiplication and division, a factor. | `x`, `y` | `src/tabliczka/exercises/service.py`, `Add.generate` and the other operations |
| minuend (odjemna) | The number a subtraction question subtracts from, `x+y`. | `minuend` | `src/tabliczka/exercises/service.py`, `Subtract.generate` |
| question | One exercise put to the learner, with its expected answer. | `Question` | `src/tabliczka/exercises/models/question.py`, `Question` |
| prompt | The text of a question as shown to the learner. | `prompt` | `src/tabliczka/exercises/models/question.py`, `Question.prompt` |
| answer | The correct result of a question. | `answer` | `src/tabliczka/exercises/models/question.py`, `Question.answer` |
| learner answer | What the learner types in reply to a question: a whole number or the stop word. | `LearnerAnswer` | `src/tabliczka/practice/service.py`, `LearnerAnswer` |
| stop word (koniec) | The word that ends a drill when typed instead of an answer. | `STOP_WORD` | `src/tabliczka/practice/service.py`, `STOP_WORD` |
| largest number (max) | The highest value of the number an operation limits: the sum for addition, the minuend for subtraction, each factor for multiplication and division. | `max_n`; `--max` on the command line | `src/tabliczka/exercises/models/operation.py`, `Operation.generate` |
| default largest number | The largest number an operation uses when the drill does not choose one: 20 for addition and subtraction, 10 for multiplication and division. | `default_max_n` | `src/tabliczka/exercises/models/operation.py`, `Operation.default_max_n` |
| number of questions (pytania) | How many questions a drill asks before the summary; without it the drill lasts until the learner stops. | `question_count`; `--pytania` on the command line | `src/tabliczka/practice/service.py`, `run_drill` |

## Scoring

| Term | Definition | Canonical identifier | Where defined |
|---|---|---|---|
| scoreboard | The record of a drill's results, printed when the drill ends. | `Scoreboard` | `src/tabliczka/practice/models/scoreboard.py`, `Scoreboard` |
| score | The counts of correct and wrong answers, for one operation or for a whole drill. | `Score` | `src/tabliczka/practice/models/score.py`, `Score` |
| correct count (dobrze) | The number of questions answered correctly. | `correct` | `src/tabliczka/practice/models/score.py`, `Score.correct` |
| wrong count (źle) | The number of questions answered wrongly. | `wrong` | `src/tabliczka/practice/models/score.py`, `Score.wrong` |
| total | The correct and wrong counts summed over all operations in a drill. | `total` | `src/tabliczka/practice/models/scoreboard.py`, `Scoreboard.total` |
| summary (Twój wynik to) | The report of the totals and each operation's score, printed when a drill ends. | `print_summary` | `src/tabliczka/practice/service.py`, `print_summary` |
| heading | The title of one operation's section in the score summary. | `heading` | `src/tabliczka/exercises/models/operation.py`, `Operation.heading` |

## Command line

| Term | Definition | Canonical identifier | Where defined |
|---|---|---|---|
| learner name (imię ucznia) | The name the program greets the learner by. | `name`; `--imie` on the command line | `src/tabliczka/ui/cli.py`, `main` |
| addition drill (dodawanie) | The command that drills addition and subtraction. | `dodawanie` | `src/tabliczka/ui/cli.py`, `dodawanie` |
| multiplication drill (mnozenie) | The command that drills multiplication and division. | `mnozenie` | `src/tabliczka/ui/cli.py`, `mnozenie` |
| operation name (działanie) | The Polish name that chooses one operation with `--dzialanie`. | keys of `OPERATION_IDS_BY_NAME`; values `dodawanie`, `odejmowanie`, `mnozenie`, `dzielenie` | `src/tabliczka/ui/cli.py`, `OPERATION_IDS_BY_NAME` |
| chosen drill (cwiczenie) | The command that drills the operations chosen with `--dzialanie`, all four when none is chosen. | `cwiczenie`; `--dzialanie` | `src/tabliczka/ui/cli.py`, `cwiczenie` |

## Spelled two ways

- **Operation names.** Classes and singletons use verbs for every operation (`Add`,
  `Subtract`, `Multiply`, `Divide`), but operation ids mix verbs and nouns (`add`,
  `subtract`, `multiplication`, `division`).
- **Learner name.** The command line option is `--imie`; the code holds it as `name`.
- **Multiplication drill.** The command is `mnozenie` (no Polish letters); the copy
  says `Mnożenie`.
## One word, two meanings

- **answer.** `Question.answer` is the correct result; the local `answer` in
  `run_drill` is what the learner typed.
- **`score`.** `Scoreboard.score` returns one operation's `Score`; the drill as a
  whole has a total, also a `Score`.
- **ćwiczenie.** The copy uses it for any drill; the `cwiczenie` command is the
  chosen drill only.
- **`correct`.** The local `correct` in `run_drill` says whether one answer was
  right; `Score.correct` is the number of right answers.
