# pompy
Pomodoro timer for your terminal to help you focus, written in Python using `curses`.

## Installation

### For end users

The recommended install path for a finished command-line app is PyPI plus `pipx`. Once the project is published, install it like this:

```bash
pipx install pompy
```

If you want to install directly from a local clone:

```bash
pipx install .
```

### For development

Use an editable install so code changes are picked up immediately without reinstalling:

```bash
python -m pip install -e .
```

After that, just rerun `pompy` in the same environment. You only need to reinstall when you change package metadata, dependencies, or packaging files.

### Prerequisites
- Python 3.8+
- `pipx` if you want the end-user install path above

## Usage
```bash
pompy [minutes] [label]
pompy [-m MINUTES] [-l LABEL]
```

Examples:

```bash
pompy
pompy 15 focus
pompy --minutes 50 --label deep work
```

## Development loop

When you are iterating on the code, keep the editable install active and run the script again after each change:

```bash
python -m pip install -e .
pompy
```

That is the fastest way to test new changes locally.

## Release

Releases are published from GitHub Actions using PyPI trusted publishing.

1. Create and push a version tag, for example `v0.1.1`.
2. Or trigger the workflow manually from the Actions tab.
3. Configure the PyPI project to trust this GitHub repository for publishing.

The workflow builds both the source distribution and wheel before publishing.

## Controls
- space — pause / resume
- q — quit

