from pathlib import Path

from desksweep.sweep import (
    MoveAction,
    execute_plan,
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
