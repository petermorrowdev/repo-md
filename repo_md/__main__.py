#!/usr/bin/env python3
"""Concatenates text files via glob patterns into a single markdown file for LLMs.

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
    repo-md '**/*.rb' '**/*.ts' --ignore-glob 'node_modules/**/*'

    # Share an entire feature's worth of code, with line numbers for debugging
    repo-md 'app/{models,controllers}/payment/**/*' --include-ln

"""

import argparse
import sys
from pathlib import Path


def collect_files(glob_patterns):
    files = set()
    for pattern in glob_patterns:
        for file_path in Path.cwd().glob(pattern):
            if file_path.is_file():
                files.add(file_path)
    return files


def process_files(glob_patterns, ignore_glob_patterns=None, include_ln=False):
    all_files = collect_files(glob_patterns)
    if ignore_glob_patterns:
        files_to_ignore = collect_files(ignore_glob_patterns)
    else:
        files_to_ignore = set()

    for file_path in all_files.difference(files_to_ignore):
        lines = []
        lines.append(f'# {file_path.relative_to(Path.cwd())}\n\n')
        lines.append('```\n')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_no, line in enumerate(f, start=1):
                    if include_ln:
                        lines.append(f'{line_no} {line}')
                    else:
                        lines.append(line)
        except UnicodeDecodeError:
            red = '\033[31m'
            bold = '\033[1m'
            reset = '\033[0m'

            sys.stderr.write(
                f'{bold}{red}UTF-8 decode error: '
                f'skip {reset}{bold}{file_path.relative_to(Path.cwd())}{reset}\n'
            )
            continue
        lines.append('```\n\n')
        print(''.join(lines))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('glob_patterns', nargs='+')
    parser.add_argument('--ignore-glob', type=str, action='append', default=None)
    parser.add_argument('--include-ln', action='store_true')
    args = parser.parse_args()
    process_files(args.glob_patterns, args.ignore_glob, args.include_ln)


if __name__ == '__main__':
    main()
