from pathlib import Path

from desksweep.sweep import (
    MoveAction,
    execute_plan,
    save_transaction,
    scan_surface,
    undo_transaction,
)


def test_scan_surface_works_without_birthtime(tmp_path: Path, monkeypatch):
    """scan_surface should not crash on platforms without st_birthtime (Linux)."""
    root = tmp_path / "Desktop"
    root.mkdir()
    (root / "a.txt").write_text("a")
    (root / "b.png").write_text("b")

    class StatNoBirth:
        st_mode = 0o100644
        st_ino = 0
        st_dev = 0
        st_nlink = 1
        st_uid = 0
        st_gid = 0
        st_size = 1
        st_atime = 1000.0
        st_mtime = 2000.0
        st_ctime = 3000.0

    def mock_stat(self, *, follow_symlinks=True):
        return StatNoBirth()

    monkeypatch.setattr(Path, "stat", mock_stat)

    files = scan_surface(root)
    assert len(files) == 2
    assert root / "a.txt" in files
    assert root / "b.png" in files


def test_execute_plan_skips_failed_moves(tmp_path: Path, monkeypatch):
    """execute_plan should skip moves that fail and continue with remaining."""
    import desksweep.sweep

    root = tmp_path / "Desktop"
    root.mkdir()

    f1 = root / "f1.txt"
    f1.write_text("1")
    f2 = root / "f2.txt"
    f2.write_text("2")

    dest1 = root / "Sub" / "f1.txt"
    dest2 = root / "Sub" / "f2.txt"

    call_count = 0
    original_move = desksweep.sweep.shutil.move

    def mock_move(src, dst, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise OSError("permission denied")
        return original_move(src, dst, **kwargs)

    monkeypatch.setattr(desksweep.sweep.shutil, "move", mock_move)

    plan = [
        MoveAction(source=f1, destination=dest1),
        MoveAction(source=f2, destination=dest2),
    ]

    succeeded = execute_plan(plan)

    assert succeeded == [MoveAction(source=f2, destination=dest2)]
    assert f1.exists()
    assert not f2.exists()
    assert dest2.exists()
    assert dest2.read_text() == "2"


def test_undo_transaction_skips_failed_moves(tmp_path: Path, monkeypatch):
    """undo_transaction should skip failed undos and continue (like execute_plan)."""
    import desksweep.sweep

    root = tmp_path / "Desktop"
    root.mkdir()

    orig1 = root / "cat.png"
    moved1 = root / "Media" / "cat.png"
    moved1.parent.mkdir()
    moved1.write_text("cat")

    orig2 = root / "dog.png"
    moved2 = root / "Media" / "dog.png"
    moved2.write_text("dog")

    transaction_dir = tmp_path / ".desksweep" / "transactions"
    tx = save_transaction(
        [
            MoveAction(source=orig1, destination=moved1),
            MoveAction(source=orig2, destination=moved2),
        ],
        transaction_dir,
    )

    call_count = 0
    original_move = desksweep.sweep.shutil.move

    def mock_move(src, dst, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise OSError("permission denied")
        return original_move(src, dst, **kwargs)

    monkeypatch.setattr(desksweep.sweep.shutil, "move", mock_move)

    undone = undo_transaction(tx)

    assert not orig1.exists()
    assert moved1.exists()
    assert orig2.exists()
    assert orig2.read_text() == "dog"
    assert not moved2.exists()

    assert undone == [MoveAction(source=moved2, destination=orig2)]


def test_save_transaction_unique_with_same_timestamp(tmp_path: Path):
    """save_transaction should produce unique filenames even with identical timestamps."""
    from unittest.mock import patch

    transaction_dir = tmp_path / ".desksweep" / "transactions"

    move = MoveAction(
        source=tmp_path / "Desktop" / "cat.png",
        destination=tmp_path / "Desktop" / "Media" / "cat.png",
    )

    fixed = __import__("datetime").datetime(2024, 1, 1, 12, 0, 0, 0)

    with patch("desksweep.sweep.datetime") as mock_dt:
        mock_dt.now.return_value = fixed
        first = save_transaction([move], transaction_dir)
        second = save_transaction([move], transaction_dir)

    assert first != second
    assert first.parent == transaction_dir
    assert second.parent == transaction_dir
    assert first.exists()
    assert second.exists()
