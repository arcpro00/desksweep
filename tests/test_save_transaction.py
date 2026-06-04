import json
from pathlib import Path

from desksweep.sweep import (
    MoveAction,
    save_transaction,
)


def test_save_transaction_creates_json_file(tmp_path: Path):
    source = tmp_path / "Desktop" / "cat.png"
    destination = tmp_path / "Desktop" / "Media" / "Images" / "cat.png"

    completed = [MoveAction(source=source, destination=destination)]

    transaction_dir = tmp_path / ".desksweep" / "transactions"

    transaction_path = save_transaction(completed, transaction_dir)

    assert transaction_path.exists()

    data = json.loads(transaction_path.read_text())

    assert data == [
        {
            "source": str(source),
            "destination": str(destination),
        }
    ]


def test_save_transaction_creates_unique_files(tmp_path: Path):
    transaction_dir = tmp_path / ".desksweep" / "transactions"

    move = MoveAction(
        source=tmp_path / "Desktop" / "cat.png",
        destination=tmp_path / "Desktop" / "Media" / "cat.png",
    )

    first = save_transaction([move], transaction_dir)
    second = save_transaction([move], transaction_dir)

    assert first.exists()
    assert second.exists()
    assert first != second
