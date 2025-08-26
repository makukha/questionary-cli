# questionary-cli
<!-- docsub: begin -->
<!-- docsub: exec yq '"> " + .project.description' pyproject.toml -->
> Command line tool for questionary
<!-- docsub: end -->

<!-- docsub: begin -->
<!-- docsub: include docs/badges.md -->
[![license](https://img.shields.io/github/license/makukha/questionary-cli.svg)](https://github.com/makukha/questionary-cli/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/questionary-cli.svg#v0.1.1)](https://pypi.org/project/questionary-cli)
[![python versions](https://img.shields.io/pypi/pyversions/questionary-cli.svg)](https://pypi.org/project/questionary-cli)
[![tests](https://raw.githubusercontent.com/makukha/questionary-cli/v0.1.1/docs/img/badge/tests.svg)](https://github.com/makukha/questionary-cli)
[![coverage](https://raw.githubusercontent.com/makukha/questionary-cli/v0.1.1/docs/img/badge/coverage.svg)](https://github.com/makukha/questionary-cli)
[![tested with multipython](https://img.shields.io/badge/tested_with-multipython-x)](https://github.com/makukha/multipython)
[![uses docsub](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/makukha/docsub/refs/heads/main/docs/badge/v1.json)](https://github.com/makukha/docsub)
[![mypy](https://img.shields.io/badge/type_checked-mypy-%231674b1)](http://mypy.readthedocs.io)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/ruff)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<!-- docsub: end -->


# Features

<!-- docsub: begin -->
<!-- docsub: include docs/features.md -->
- Command line utility for [questionary](https://questionary.readthedocs.io)
- All question types and prompts supported
- Output as JSON or plain text 
- Chain multiple questions
<!-- docsub: end -->


# Installation

```shell
$ pip install questionary-cli
```


# Usage

<!-- docsub: begin #usage.md -->
<!-- docsub: include docs/usage.md -->
_To be documented._
<!-- docsub: end #usage.md -->


# CLI Reference

<!-- docsub: begin #cli.md -->
<!-- docsub: include docs/cli.md -->
<!-- docsub: begin -->
<!-- docsub: help que -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que --help
Usage: que [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Command line utility for questionary.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ --json   -j        Output results in JSON format.                                │
│ --plain  -p        Output results in plain text, one value per line.             │
│ --file   -f  FILE  Output results to file instead of stdout.                     │
│ --help             Show this message and exit.                                   │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────╮
│ autocomplete             Autocomplete text prompt.                               │
│ checkbox                 Multi-select checkbox prompt.                           │
│ confirm                  Confirmation prompt.                                    │
│ password                 Password prompt.                                        │
│ path                     Filesystem path prompt.                                 │
│ print                    Print formatted text.                                   │
│ rawselect                Raw select option prompt.                               │
│ select                   Select option prompt.                                   │
│ text                     Text prompt.                                            │
│ wait                     Wait until any key is pressed.                          │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Text

<!-- docsub: begin -->
<!-- docsub: help que text -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que text --help
Usage: que text [OPTIONS]

Text prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt       -p  TEXT  Prompt text to be displayed. [required]              │
│ *  --key,--as     -k  TEXT  Question key to be used in output. [required]        │
│    --default      -d  TEXT  Default value if no text is entered. [default: ""]   │
│    --instruction  -i  TEXT  Instruction displayed to the user. [default: ""]     │
│    --multiline    -m        Allow multiline text to be entered.                  │
│    --help                   Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Password

<!-- docsub: begin -->
<!-- docsub: help que password -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que password --help
Usage: que password [OPTIONS]

Password prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt    -p  TEXT  Prompt text to be displayed. [required]                 │
│ *  --key,--as  -k  TEXT  Question key to be used in output. [required]           │
│    --default   -d  TEXT  Default value if no text is entered. [default: ""]      │
│    --help                Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Path

<!-- docsub: begin -->
<!-- docsub: help que path -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que path --help
Usage: que path [OPTIONS]

Filesystem path prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt    -p  TEXT  Prompt text to be displayed. [required]                 │
│ *  --key,--as  -k  TEXT  Question key to be used in output. [required]           │
│    --help                Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Confirm

<!-- docsub: begin -->
<!-- docsub: help que confirm -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que confirm --help
Usage: que confirm [OPTIONS]

Confirmation prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt       -p  TEXT  Prompt text to be displayed. [required]              │
│    --key,--as     -k  TEXT  Question key to be used in output.                   │
│    --default      -d        Default value if no text is entered.                 │
│                             [default: False]                                     │
│    --instruction  -i  TEXT  Instruction displayed to the user. [default: ""]     │
│    --auto-enter   -a        No need to press Enter after "y" or "n" is pressed.  │
│    --exit-code    -e        Exit with code 1 "n" is entered.                     │
│    --help                   Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Select

<!-- docsub: begin -->
<!-- docsub: help que select -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que select --help
Usage: que select [OPTIONS]

Select option prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt       -p  TEXT  Prompt text to be displayed. [required]              │
│ *  --key,--as     -k  TEXT  Question key to be used in output. [required]        │
│ *  --choices      -c  TEXT  Choices as JSON encoded list of strings. [required]  │
│    --default      -d  TEXT  Default value if no text is entered.                 │
│    --instruction  -i  TEXT  Instruction displayed to the user. [default: ""]     │
│    --help                   Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Raw Select

<!-- docsub: begin -->
<!-- docsub: help que rawselect -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que rawselect --help
Usage: que rawselect [OPTIONS]

Raw select option prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt    -p  TEXT  Prompt text to be displayed. [required]                 │
│ *  --key,--as  -k  TEXT  Question key to be used in output. [required]           │
│    --help                Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Checkbox

<!-- docsub: begin -->
<!-- docsub: help que checkbox -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que checkbox --help
Usage: que checkbox [OPTIONS]

Multi-select checkbox prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt    -p  TEXT  Prompt text to be displayed. [required]                 │
│ *  --key,--as  -k  TEXT  Question key to be used in output. [required]           │
│    --help                Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Autocomplete

<!-- docsub: begin -->
<!-- docsub: help que autocomplete -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que autocomplete --help
Usage: que autocomplete [OPTIONS]

Autocomplete text prompt.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt    -p  TEXT  Prompt text to be displayed. [required]                 │
│ *  --key,--as  -k  TEXT  Question key to be used in output. [required]           │
│    --help                Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Press Any Key To Continue...

<!-- docsub: begin -->
<!-- docsub: help que wait -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que wait --help
Usage: que wait [OPTIONS]

Wait until any key is pressed.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --prompt  -p  TEXT  Prompt text to be displayed.                              │
│                        [default: Press any key to continue...]                   │
│                        [required]                                                │
│    --append  -a        When option is set, append " press any key to             │
│                        continue..." to the prompt.                               │
│    --help              Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->

## Print

<!-- docsub: begin -->
<!-- docsub: help que print -->
<!-- docsub: lines after 2 upto -1 -->
<!-- docsub: strip -->
```shell
$ que print --help
Usage: que print [OPTIONS]

Print formatted text.

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ *  --text  -t  TEXT  Text to be printed. [required]                              │
│    --help            Show this message and exit.                                 │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
<!-- docsub: end -->
<!-- docsub: end #cli.md -->


# Contributing

Pull requests, feature requests, and bug reports are welcome!

* [Contribution guidelines](https://github.com/makukha/questionary-cli/blob/main/.github/CONTRIBUTING.md)


# Authors

* Michael Makukha


# See also

* [Documentation](https://github.com/makukha/questionary-cli#readme)
* [Issues](https://github.com/makukha/questionary-cli/issues)
* [Changelog](https://github.com/makukha/questionary-cli/blob/main/CHANGELOG.md)
* [Security Policy](https://github.com/makukha/questionary-cli/blob/main/.github/SECURITY.md)
* [Contribution Guidelines](https://github.com/makukha/questionary-cli/blob/main/.github/CONTRIBUTING.md)
* [Code of Conduct](https://github.com/makukha/questionary-cli/blob/main/.github/CODE_OF_CONDUCT.md)
* [License](https://github.com/makukha/questionary-cli/blob/main/LICENSE)
