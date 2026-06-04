from dataclasses import dataclass
from pathlib import Path


@dataclass
class MoveAction:
    source: Path
    destination: Path

def scan_surface(root: Path, ignore_hidden: bool = True) -> list[Path]:
    """Returns loose file paths directly inside root (not subdirectories)"""
    ...


def build_plan(
    files: list[Path],
    root: Path,
    rules: dict[str, list[str]],
    default_folder: str = "Review",
) -> list[MoveAction]:
    """Decide where files should move without moving them."""
    ...


def execute_plan(plan: list[MoveAction]) -> list[MoveAction]:
    """Move files and return only the moves that succeeded"""
    ...


def save_transaction(
    completed_moves: list[MoveAction],
    transaction_dir: Path,
) -> Path:
    """Save completed moves to a JSON file and return its path"""
    ...


def undo_transaction(transaction_path: Path) -> list[MoveAction]:
    """Read a transaction file and move files back"""
    ...