from pathlib import Path

from desksweep.sweep import (
    MoveAction,
    build_plan,
    execute_plan,
    save_transaction,
    scan_surface,
    undo_transaction,
)

random_names = ["asdoifj-rg0","23ghdsFSH","__iwhaiguehwi0198275","LJLJLJ","Whats-is-up-bro"]

def test_scan_surface_returns_only_loose_files(tmp_path: Path):
    root = tmp_path / "Desktop"
    root.mkdir()
    loose_files = []
    for name in random_names:
        loose_file = root / f"{name}.png"
        loose_file.write_text("fake image")
        loose_files.append(loose_file)

        folder = root / name
        folder.mkdir()
        nested_file = folder / "important.png"
        nested_file.write_text("do not touch")


    files = scan_surface(root)

    assert files == loose_files


def test_scan_surface_ignores_hidden_files(tmp_path: Path):
    root = tmp_path / "Desktop"
    root.mkdir()

    visible = root / "notes.pdf"
    visible.write_text("notes")

    for word in ["secret","pog","huh","why"]:
        hidden = root / f".{word}"
        hidden.write_text("secret")

    files = scan_surface(root, ignore_hidden=True)

    assert files == [visible]