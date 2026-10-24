from random import randint, choice

import click
from click import Abort


@click.group()
@click.argument("name", type=str, required=True)
def main(name: str) -> None:
    click.echo(f"Witaj {name}!")

@main.command()
def dodawanie() -> None:
    click.echo(f"Nauczymy się dodawnia i odejmowania!")
    result = {
        "substract": {"ok": 0, "bad": 0},
        "add": {"ok": 0, "bad": 0},
    }
    try:
        while True:
            is_substract = choice([True, False])
            x = randint(1, 10)
            y = randint(1, 10)
            suma = x+y
            if is_substract:
                wynik = click.prompt(f"Odejmowanie: Ile to {suma}-{x}?", type=int)
                correct_answer = y
            else:
                wynik = click.prompt(f"Dodawanie: Ile to {x}+{y}?", type=int)
                correct_answer = suma
            if wynik == correct_answer:
                click.echo(click.style("Dobrze!", fg="green"))
                result[("substract" if is_substract else "add")]["ok"] += 1
            else:
                click.echo(click.style(f"Niestety, źle, prawidłowy wynik to {correct_answer}.", fg="red"))
                result[("substract" if is_substract else "add")]["bad"] += 1
    except Abort:
        click.echo("\n")
        click.echo("="*20)
        click.echo("Twój wynik to:")
        ok = result["add"]["ok"] + result["substract"]["ok"]
        bad = result["add"]["bad"] + result["substract"]["bad"]
        click.echo(click.style(f"{ok} - dobrze", fg="green"))
        if bad:
            click.echo(click.style(f"{bad} - źle", fg="red"))

        click.echo("="*20)
        click.echo("Dodawnia:")
        click.echo(click.style(f"{result['add']['ok']} - dobrze", fg="green"))
        if bad:
            click.echo(click.style(f"{result['add']['bad']} - źle", fg="red"))
        click.echo("="*20)
        click.echo("Odejmowanie:")
        click.echo(click.style(f"{result['substract']['ok']} - dobrze", fg="green"))
        if bad:
            click.echo(click.style(f"{result['substract']['bad']} - źle", fg="red"))



@main.command()
def mnozenie() -> None:
    click.echo(f"Nauczymy się tabliczki mnożenia i dzielenia!")
    result = {
        "division": {"ok": 0, "bad": 0},
        "multiplication": {"ok": 0, "bad": 0},
    }
    try:
        while True:
            is_division = choice([True, False])
            x = randint(1, 10)
            y = randint(1, 10)
            product = x*y
            if is_division:
                wynik = click.prompt(f"Dzielenie: Ile to {product}:{x}?", type=int)
                correct_answer = y
            else:
                wynik = click.prompt(f"Mnożenie: Ile to {x}x{y}?", type=int)
                correct_answer = product
            if wynik == correct_answer:
                click.echo(click.style("Dobrze!", fg="green"))
                result[("division" if is_division else "multiplication")]["ok"] += 1
            else:
                click.echo(click.style(f"Niestety, źle, prawidłowy wynik to {correct_answer}.", fg="red"))
                result[("division" if is_division else "multiplication")]["bad"] += 1
    except Abort:
        click.echo("\n")
        click.echo("="*20)
        click.echo("Twój wynik to:")
        ok = result["multiplication"]["ok"] + result["division"]["ok"]
        bad = result["multiplication"]["bad"] + result["division"]["bad"]
        click.echo(click.style(f"{ok} - dobrze", fg="green"))
        if bad:
            click.echo(click.style(f"{bad} - źle", fg="red"))

        click.echo("="*20)
        click.echo("Mnożenie:")
        click.echo(click.style(f"{result['multiplication']['ok']} - dobrze", fg="green"))
        if bad:
            click.echo(click.style(f"{result['multiplication']['bad']} - źle", fg="red"))
        click.echo("="*20)
        click.echo("Dzielenie:")
        click.echo(click.style(f"{result['division']['ok']} - dobrze", fg="green"))
        if bad:
            click.echo(click.style(f"{result['division']['bad']} - źle", fg="red"))


if __name__ == "__main__":
    main()