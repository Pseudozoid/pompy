# pompy

A simple Pomodoro timer for your terminal.

Use it to stay focused in timed work sessions without leaving the command line.

## Install

`pompy` is distributed on PyPI as `pompy-timer`.

If you already have `pipx`:

```bash
pipx install pompy-timer
```

If you do not have `pipx` yet:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Restart your terminal, then run:

```bash
pipx install pompy-timer
```

## Quick Start

Start a standard 25-minute session:

```bash
pompy
```

Start a custom session:

```bash
pompy 15
pompy 50 "Deep work"
```

You can also use flags:

```bash
pompy --minutes 30 --label "Code review"
```

Run multiple Pomodoro cycles with automatic breaks:

```bash
pompy --cycles 4 --break 5 --long-break 15 --label "Study"
pompy -c 4 -b 5 -B 15 -l "Study"
```

Control the transition screen between phases:

```bash
pompy --transition-seconds 3
pompy --transition-wait-key
pompy -t 3
pompy -w
```

Choose a large timer digit style:

```bash
pompy --digit-style block
pompy --digit-style outline
pompy --digit-style segment
pompy -d minimal
```

Defaults:

- `--cycles` is `1`
- `--break` is `5` minutes
- `--long-break` is `15` minutes
- `--transition-seconds` is `2.0`

## While The Timer Runs

- `space` to pause or resume
- `q` to quit early

## Common Commands

Show help:

```bash
pompy --help
```

Show version:

```bash
pompy --version
```

Update:

```bash
pipx upgrade pompy-timer
```

Uninstall:

```bash
pipx uninstall pompy-timer
```

