# pompy
Pomodoro timer for your terminal to help you focus, written in Python using `curses`.

## Installation

### Prerequisites
- Python 3.8+
- `pipx` installed

If you don’t have `pipx` yet:

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```
Restart your shell after this.
### Install with pipx (recommended)
From GitHub:
`pipx install git+https://github.com/yourusername/pompy.git`

Or from a local clone:
`pipx install .`

## Usage
```bash
pompy [minutes] [label]
```

## Controls
- space — pause / resume
- q — quit

