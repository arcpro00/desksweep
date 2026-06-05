# desksweep

Organizes stray files on your desktop into folders by file type. Preview
before moving, then undo with a single command if you change your mind.

## Installation

First install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you
don't have it already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install desksweep:

```bash
uv pip install git+https://github.com/user/desksweep.git
```

## Usage

Preview where files would land (no files are moved):

```bash
desksweep preview ~/Desktop
```

Move files into categorized folders and save a transaction for undo:

```bash
desksweep clean ~/Desktop
```

Reverse a previous clean using its saved transaction:

```bash
desksweep undo ~/.desksweep/transactions/<id>.json
```

Override the built-in file-type rules with your own config (a JSON object
mapping folder names to extension lists):

```bash
desksweep clean ~/Desktop --config ~/my-rules.json
```

```json
{
    "Code": [".py", ".js", ".ts", ".rs"],
    "Images": [".jpg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"]
}
```

Unmatched extensions land in a `Review/` folder.
