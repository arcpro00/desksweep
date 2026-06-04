from pathlib import Path

from desksweep.sweep import (
    MoveAction,
    build_plan,
    execute_plan,
    save_transaction,
    scan_surface,
    undo_transaction,
)

def test_undo_transaction_restores_files(tmp_path: Path):
    root = tmp_path / "Desktop"
    root.mkdir()

    original = root / "cat.png"
    moved = root / "Media" / "Images" / "cat.png"

    moved.parent.mkdir(parents=True)
    moved.write_text("fake image")

    transaction_dir = tmp_path / ".desksweep" / "transactions"

    completed = [MoveAction(source=original, destination=moved)]
    transaction_path = save_transaction(completed, transaction_dir)

    undone = undo_transaction(transaction_path)

    assert original.exists()
    assert original.read_text() == "fake image"
    assert not moved.exists()

    assert undone == [
        MoveAction(source=moved, destination=original)
    ]

def test_undo_uses_only_given_transaction_file(tmp_path: Path):
    root = tmp_path / "Desktop"
    root.mkdir()

    original_cat = root / "cat.png"
    moved_cat = root / "Media" / "cat.png"
    moved_cat.parent.mkdir(parents=True)
    moved_cat.write_text("cat")

    original_dog = root / "dog.png"
    moved_dog = root / "Media" / "dog.png"
    moved_dog.write_text("dog")

    transaction_dir = tmp_path / ".desksweep" / "transactions"

    cat_tx = save_transaction(
        [MoveAction(source=original_cat, destination=moved_cat)],
        transaction_dir,
    )

    save_transaction(
        [MoveAction(source=original_dog, destination=moved_dog)],
        transaction_dir,
    )

    undone = undo_transaction(cat_tx)

    assert original_cat.exists()
    assert original_cat.read_text() == "cat"
    assert not moved_cat.exists()

    assert not original_dog.exists()
    assert moved_dog.exists()
    assert moved_dog.read_text() == "dog"

    assert undone == [
        MoveAction(source=moved_cat, destination=original_cat)
    ]