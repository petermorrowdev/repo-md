# repo-md

Concatenates text files via glob patterns into a single markdown file for LLMs.

Useful when working with non-agentic LLMs or when you want precise control over the
assistants context window.

`repo-md` relies only on the python standard library (`pathlib`, `sys` & `argparse`)
and works with all modern python versions (3.10+).


## Installation

You can install with `uv`

```bash
uv tool install git+https://github.com/petermorrowdev/repo-md
```

Or vanilla `pip`

```bash
pip install git+https://github.com/petermorrowdev/repo-md
```

## Usage

```
$ repo-md --help
usage: repo-md [-h] [--ignore-glob IGNORE_GLOB] [--include-ln]
               glob_patterns [glob_patterns ...]

Collects code via glob patterns into a single markdown file for LLM context.

This script processes one or more glob patterns to create a formatted markdown output
of source code files, designed for sharing with Large Language Models (LLMs).

For each matching file, it outputs:
- A markdown header with the relative file path.
- Source code content enclosed in a language-specific fenced markdown block.

The default output is token-efficient (no line numbers). Use --include-ln for specific
line-based LLM feedback.

Usage:
    repo-md [options] <glob_pattern> [<glob_pattern> ...]

Options:
    --include-ln    Includes line numbers
    --ignore-glob   Glob pattern(s) to exclude files

Examples:
    # Share model and specs, excluding node_modules/ build files
    repo-md '**/*.rb' '**/*_spec.rb' --ignore-glob 'node_modules/**/*'

    # Share an entire feature's worth of code, with line numbers for debugging
    repo-md 'app/{models,controllers}/payment/**/*' --include-ln

positional arguments:
  glob_patterns

options:
  -h, --help            show this help message and exit
  --ignore-glob IGNORE_GLOB
  --include-ln
```
