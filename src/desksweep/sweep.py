import json
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from desksweep.config import DEFAULT_RULES


@dataclass
class MoveAction:
    source: Path
    destination: Path


def _scan_sort_key(p: Path) -> float:
    stat = p.stat()
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_ctime


def scan_surface(root: Path, ignore_hidden: bool = True) -> list[Path]:
    files: list[Path] = []
    for entry in root.iterdir():
        if not entry.is_file():
            continue
        if ignore_hidden and entry.name.startswith("."):
            continue
        files.append(entry)
    files.sort(key=_scan_sort_key)
    return files


def build_plan(
    files: list[Path],
    root: Path,
    rules: dict[str, list[str]] | None = None,
    default_folder: str = "Review",
) -> list[MoveAction]:
    if rules is None:
        rules = DEFAULT_RULES
    plan: list[MoveAction] = []
    for file in files:
        matched = False
        for category, extensions in rules.items():
            if file.suffix in extensions:
                plan.append(
                    MoveAction(
                        source=file,
                        destination=root / category / file.name,
                    )
                )
                matched = True
                break
        if not matched:
            plan.append(
                MoveAction(
                    source=file,
                    destination=root / default_folder / file.name,
                )
            )
    return plan


def execute_plan(plan: list[MoveAction]) -> list[MoveAction]:
    succeeded: list[MoveAction] = []
    for action in plan:
        try:
            action.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(action.source), str(action.destination))
            succeeded.append(action)
        except Exception:
            continue
    return succeeded


def save_transaction(
    completed_moves: list[MoveAction],
    transaction_dir: Path,
) -> Path:
    transaction_dir.mkdir(parents=True, exist_ok=True)
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    transaction_path = transaction_dir / f"{timestamp}-{unique_id}.json"
    data = [
        {"source": str(move.source), "destination": str(move.destination)}
        for move in completed_moves
    ]
    transaction_path.write_text(json.dumps(data))
    return transaction_path


def undo_transaction(transaction_path: Path) -> list[MoveAction]:
    data = json.loads(transaction_path.read_text())
    undone: list[MoveAction] = []
    for entry in data:
        source = Path(entry["destination"])
        destination = Path(entry["source"])
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            undone.append(MoveAction(source=source, destination=destination))
        except Exception:
            continue
    return undone
