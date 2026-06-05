import json
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_RULES: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".csv", ".json", ".xml"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Archives": [".zip", ".tar", ".gz", ".bz2", ".7z", ".rar"],
}

CONFIG_DIR = Path.home() / ".desksweep"
CONFIG_PATH = CONFIG_DIR / "config.json"


def load_rules(config_path: Optional[Path] = None) -> Dict[str, List[str]]:
    if config_path is None and CONFIG_PATH.exists():
        config_path = CONFIG_PATH

    if config_path is not None and config_path.exists():
        data = json.loads(config_path.read_text())
        if isinstance(data, dict):
            return {
                str(category): [str(e) for e in extensions]
                for category, extensions in data.items()
                if isinstance(extensions, list)
            }

    return dict(DEFAULT_RULES)
