from pathlib import Path

import typer

from desksweep.sweep import (
    build_plan,
    execute_plan,
    save_transaction,
    scan_surface,
    undo_transaction,
)

app = typer.Typer()


@app.command()
def preview(root: Path):
    files = scan_surface(root)
    plan = build_plan(files, root)

    for action in plan:
        typer.echo(f"{action.source} -> {action.destination}")


@app.command()
def clean(root: Path):
    files = scan_surface(root)
    plan = build_plan(files, root)
    completed = execute_plan(plan)

    transaction_path = save_transaction(
        completed,
        Path.home() / ".desksweep" / "transactions",
    )

    typer.echo(f"Moved {len(completed)} files.")
    typer.echo(f"Saved transaction: {transaction_path}")


@app.command()
def undo(transaction_path: Path):
    undone = undo_transaction(transaction_path)
    typer.echo(f"Undid {len(undone)} moves.")
