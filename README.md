# Linebreaker

Intelligent line breaking for Markdown and text files, with support for:
- Citations in format `[@...]`
- Decimal numbers
- Common abbreviations (Dr., Prof., vs., et al., etc.)
- YAML headers
- Code blocks
- Soft breaks on conjunctions, commas, and/or

## Installation

Install from PyPI using pixi:

```bash
pixi add linebreaker
```

Or install from source:

```bash
git clone https://github.com/silas/linebreaker.git
cd linebreaker
pixi install
```

## Usage

### As a command-line tool:

```bash
# Process a single file
linebreaker your_file.qmd

# Process a directory
linebreaker writing/

# For compatibility, you can still use the old script
python -m linebreaker.cli your_file.qmd
```

### As a module:

```python
from linebreaker import format_line, break_text

# Format a single line
result = format_line("Your text here...")

# Process entire text with YAML/code blocks
result = break_text(full_text)
```

## Running Tests

```bash
# Run all tests
pytest linebreaker/tests/

# Run with verbose output
pytest linebreaker/tests/ -v

# Run specific test file
pytest linebreaker/tests/test_core.py -v
```

## Project Structure

```
linebreaker/
├── src/
│   └── linebreaker/
│       ├── __init__.py          # Package exports
│       ├── core.py              # Core line breaking logic
│       ├── cli.py               # Command-line interface
│       └── tests/
│           ├── __init__.py
│           └── test_core.py     # Test suite
├── pyproject.toml               # Package configuration
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## Features

### Hard Breaks (Sentence Boundaries)
- Splits on `.`, `?`, `!` when both before and after have 20+ characters
- Avoids common abbreviations: vs., Dr., Prof., Mr., Mrs., Ms., Ph.D., M.D., Jr., Sr., etc., e.g., i.e., et al., vol., no., pp., fig.

### Medium Breaks (Colons/Semicolons)
- Splits sentences longer than 80 characters at `:` or `;`
- Only if both parts have 20+ characters

### Soft Breaks (Conjunctions)
- Applied when there are 3+ sentences or sentence is >60 characters
- Breaks on: `but`, `such as`, `for example`, `e.g.`, `i.e.` (after 20 chars)
- Breaks on commas (after 40 chars)
- Breaks on `and`, `or` (after 40 chars)

### Smart Masking
- Citations `[@...]` are masked to prevent dots inside from triggering breaks
- Decimal numbers like `0.85` are masked similarly

## Development

To add new abbreviations, edit the `abbreviations` pattern in `core.py`:

```python
abbreviations = r'(?!vs\.|dr\.|prof\.|...|your_abbrev\.)'
```
