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

Share all Python and TypeScript files in the current directory and subdirectories.

```bash
repo-md '**/*.py' '**/*.ts' | pbcopy
```

Share only core Rails components (models and controllers).

```bash
repo-md 'app/{models,controllers}/**/*.rb' | xclip
```

Use the --ignore-glob flag to exclude files from build tools, dependencies, or caches.

```bash
repo-md '**/*.go' --ignore-glob 'vendor/**/*'
```

Include line numbers when you want to ask the LLM "needle in haystack" style questions
like "Where do we call the stripe API? Respond with precise path and line numbers."

```bash
repo-md 'src/features/checkout/**/*' --include-ln
```

This provides the LLM with the complete source code and the Cargo.toml dependency file.

```bash
repo-md 'src/features/checkout/**/*' --include-ln
```
