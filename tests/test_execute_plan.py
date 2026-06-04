from pathlib import Path

from desksweep.sweep import (
    MoveAction,
    build_plan,
    execute_plan,
    save_transaction,
    scan_surface,
    undo_transaction,
)

def test_execute_plan_moves_files(tmp_path: Path):
    root = tmp_path / "Desktop"
    root.mkdir()

    source = root / "cat.png"
    source.write_text("fake image")

    destination = root / "Media" / "Images" / "cat.png"

    plan = [MoveAction(source=source, destination=destination)]

    completed = execute_plan(plan)

    assert completed == plan
    assert not source.exists()
    assert destination.exists()
    assert destination.read_text() == "fake image"
