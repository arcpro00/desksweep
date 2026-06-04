# desksweep

Command-line tool to organize stray files on the desktop by file type.

## Usage

```bash
# Preview what would happen (no files are moved)
desksweep preview ~/Desktop

# Organize files into folders by type
desksweep clean ~/Desktop

# Undo the last clean using its saved transaction
desksweep undo ~/.desksweep/transactions/<transaction-id>.json
```

### Example

Before (`~/Desktop`):
```
photo.jpg  report.pdf  song.mp3  notes.txt  meeting.mp4  script.py
```

### Preview

```bash
$ desksweep preview ~/Desktop
/Users/you/Desktop/photo.jpg -> /Users/you/Desktop/Images/photo.jpg
/Users/you/Desktop/report.pdf -> /Users/you/Desktop/Documents/report.pdf
/Users/you/Desktop/song.mp3 -> /Users/you/Desktop/Audio/song.mp3
/Users/you/Desktop/notes.txt -> /Users/you/Desktop/Documents/notes.txt
/Users/you/Desktop/meeting.mp4 -> /Users/you/Desktop/Video/meeting.mp4
/Users/you/Desktop/script.py -> /Users/you/Desktop/Review/script.py
```

### Clean

```bash
$ desksweep clean ~/Desktop
Moved 6 files.
Saved transaction: /Users/you/.desksweep/transactions/20260604T205832848891-8c1d81…json
```

After `clean`:
```
Desktop/
├── Audio/
│   └── song.mp3
├── Documents/
│   ├── notes.txt
│   └── report.pdf
├── Images/
│   └── photo.jpg
├── Review/
│   └── script.py
└── Video/
    └── meeting.mp4
```

### Undo

```bash
$ desksweep undo /Users/you/.desksweep/transactions/20260604T205832848891-8c1d81…json
Undid 6 moves.
```

All files are moved back to their original locations.

## Configuration

Customize which file extensions go into which folders by creating `~/.desksweep/config.json`:

```json
{
    "Code": [".py", ".js", ".ts", ".rs", ".go"],
    "Images": [".jpg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"]
}
```

When a config file exists, it **fully replaces** the built-in defaults. You can also point to a different file with `--config`:

```bash
desksweep preview ~/Desktop --config ~/my-rules.json
desksweep clean ~/Desktop -c ~/my-rules.json
```

Files whose extension doesn't match any rule are placed in a `Review/` folder.
```
