from pathlib import Path

from desksweep.sweep import (
    MoveAction,
    build_plan,
)


def test_build_plan_moves_known_file_types(tmp_path: Path):
    root = tmp_path / "Desktop"
    root.mkdir()

    image = root / "cat.png"
    image.write_text("fake image")

    pdf = root / "notes.pdf"
    pdf.write_text("notes")

    rules = {"Media/Images": [".png", ".jpg"], "Documents": [".pdf"]}

    plan = build_plan([image, pdf], root, rules)

    assert plan == [
        MoveAction(source=image, destination=root / "Media" / "Images" / "cat.png"),
        MoveAction(source=pdf, destination=root / "Documents" / "notes.pdf"),
    ]


def test_build_plan_moves_unknown_files_to_review(tmp_path: Path):
    root = tmp_path / "Desktop"
    root.mkdir()

    unknown = root / "weird.xyz"
    unknown.write_text("unknown")

    rules = {
        "Media/Images": [".png", ".jpg"],
    }

    plan = build_plan([unknown], root, rules, default_folder="Review")

    assert plan == [
        MoveAction(source=unknown, destination=root / "Review" / "weird.xyz")
    ]
