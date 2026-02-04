#!/usr/bin/env python3
"""Covert a glob of code files to a single markdown file for LLM context.

This script processes one or more glob patterns to create a formatted markdown output
of source code files, designed for sharing with Large Language Models (LLMs). For each
matching file, it outputs:
- A markdown header with the file path
- Line-numbered source code content enclosed in markdown separators

Perfect for sharing context about Rails components, models, controllers, or entire
features with LLMs.

Usage:
    repo-md <glob_pattern> [<glob_pattern> ...]

Examples:
    # Share a specific model and its specs
    repo-md '**/*.rb' '**/*.js' | pbcopy
    # <PASTE> into the LLM prompt with your question

    # Share an entire feature's worth of code
    repo-md 'app/{models,controllers,views,components}/payment/**/*'

The script outputs to stdout, so you can pipe to clipboard:
    repo-md '**/*.rb' '**/*.js' | pbcopy
    repo-md '**/*.py' '**/*.ts' | xclip

Installation:
1. Save this script as /usr/local/bin/repo-md:
    curl -o /usr/local/bin/repo-md https://gist.githubusercontent.com/petermorrowdev/4ed6cb3f87524973e0036a9e22e67b9f/raw/4e3e5bb7831c37e47cd9e9bf631765adfb7af801/repo-md

2. Make it executable:
    chmod +x /usr/local/bin/repo-md

Now you can use repo-md from any directory to quickly share code context with LLMs.
"""

import argparse
from pathlib import Path


def collect_globs(glob_patterns):
    globs = set()
    for pattern in glob_patterns:
        for file_path in Path.cwd().glob(pattern):
            if file_path.is_file():
                globs.add(file_path)
    return globs


def process_files(glob_patterns, ignore_glob_patterns=None, exclude_ln=False):
    globs_to_print = collect_globs(glob_patterns)
    if ignore_glob_patterns:
        globs_to_ignore = collect_globs(ignore_glob_patterns)
    else:
        globs_to_ignore = set()

    for file_path in globs_to_print.difference(globs_to_ignore):
        print(f"# {file_path.relative_to(Path.cwd())}\n")
        print("```")
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if exclude_ln:
                    print(line, end="")
                else:
                    print(line_no, line, end="")
        print("```\n\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "glob_patterns",
        nargs="+",
    )
    parser.add_argument("--ignore-glob", type=str, action="append", default=None)
    parser.add_argument("--exclude-ln", action="store_true")
    args = parser.parse_args()
    process_files(args.glob_patterns, args.ignore_glob, args.exclude_ln)


if __name__ == "__main__":
    main()
