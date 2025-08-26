import json
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
from pathlib import Path
from sys import stdout
from typing import Any, Callable

import questionary as q
import rich_click as click
from typing_extensions import ParamSpec, TextIO, TypeAlias, TypeVar

P = ParamSpec('P')
R = TypeVar('R')
F: TypeAlias = Callable[P, R]
Key: TypeAlias = str | object


class OutputType(str, Enum):
    JSON = auto()
    PLAIN = auto()


@dataclass(kw_only=True)
class Context:
    questions: dict[Key, q.Question] = field(default_factory=dict)
    output: OutputType | None
    file: str | TextIO
    confirm_exit_nonzero: set[Key] = field(default_factory=set)


# Group


@click.group(chain=True)
@click.option(
    '-j',
    '--json',
    is_flag=True,
    help='Output results in JSON format.',
)
@click.option(
    '-p',
    '--plain',
    is_flag=True,
    help='Output results in plain text, one value per line.',
)
@click.option(
    '-f',
    '--file',
    type=click.Path(dir_okay=False),
    help='Output results to file instead of stdout.',
)
@click.pass_context
def cli(
    ctx: click.Context,
    json: bool,
    plain: bool,
    file: str | None,
) -> None:
    """
    Command line utility for questionary.
    """
    if json and plain:
        raise click.UsageError('Incompatible options --json and --plain.')
    elif json:
        output = OutputType.JSON
    elif plain:
        output = OutputType.PLAIN
    else:
        output = None

    ctx.obj = Context(
        output=output,
        file=stdout if file is None else file,
    )


# Reusable decorators


pass_context = click.make_pass_decorator(Context, ensure=True)


def command(**kwargs: Any) -> Callable[[F[P, R]], F[P, R]]:
    return lambda f: wraps(f)(
        cli.command(
            context_settings=dict(show_default=True),
            **kwargs,
        )(f)
    )


def option_choices(**kwargs: Any) -> Callable[[F[P, R]], F[P, R]]:
    return lambda f: wraps(f)(
        click.option(
            '-c',
            '--choices',
            help='Choices as JSON encoded list of strings.',
            required=True,
            **kwargs,
        )(f)
    )


def option_default(v: Any = None, **kwargs: Any) -> Callable[[F[P, R]], F[P, R]]:
    return lambda f: wraps(f)(
        click.option(
            '-d',
            '--default',
            default=v,
            help='Default value if no text is entered.',
            **kwargs,
        )(f)
    )


def option_instruction(**kwargs: Any) -> Callable[[F[P, R]], F[P, R]]:
    return lambda f: wraps(f)(
        click.option(
            '-i',
            '--instruction',
            help='Instruction displayed to the user.',
            **(dict(default='') | kwargs),
        )(f)
    )


def option_key(**kwargs: Any) -> Callable[[F[P, R]], F[P, R]]:
    return lambda f: wraps(f)(
        click.option(
            '-k',
            '--key',
            '--as',
            help='Question key to be used in output.',
            **(dict(required=True) | kwargs),
        )(f)
    )


def option_prompt(**kwargs: Any) -> Callable[[F[P, R]], F[P, R]]:
    return lambda f: wraps(f)(
        click.option(
            '-p',
            '--prompt',
            help='Prompt text to be displayed.',
            **(dict(required=True) | kwargs),
        )(f)
    )


# Commands and callbacks


@command()
@option_prompt()
@option_key()
@option_default('')
@option_instruction()
@click.option(
    '-m',
    '--multiline',
    is_flag=True,
    default=False,
    help='Allow multiline text to be entered.',
)
@pass_context
def text(
    ctx: Context,
    prompt: str,
    key: str,
    default: str,
    instruction: str,
    multiline: bool,
) -> None:
    """
    Text prompt.
    """
    assert_unique_key(key, ctx)
    ctx.questions[key] = q.text(
        message=prompt,
        default=default,
        instruction=f'{instruction}: ' if instruction else '',
        multiline=multiline,
    )


@command()
@option_prompt()
@option_key()
@option_default('')
@pass_context
def password(
    ctx: Context,
    prompt: str,
    key: str,
    default: str,
) -> None:
    """
    Password prompt.
    """
    assert_unique_key(key, ctx)
    ctx.questions[key] = q.password(
        message=prompt,
        default=default,
    )


@command()
@option_prompt()
@option_key()
@pass_context
def path(
    ctx: Context,
    prompt: str,
    key: str,
) -> None:
    """
    Filesystem path prompt.
    """
    assert_unique_key(key, ctx)
    raise NotImplementedError  # todo


@command()
@option_prompt()
@option_key(required=False)
@option_default(False)
@option_instruction()
@click.option(
    '-a',
    '--auto-enter',
    is_flag=True,
    default=False,
    help='No need to press Enter after "y" or "n" is pressed.',
)
@click.option(
    '-e',
    '--exit-code',
    is_flag=True,
    default=False,
    help='Exit with code 1 "n" is entered.',
)
@pass_context
def confirm(
    ctx: Context,
    prompt: str,
    key: str | None,
    default: bool,
    instruction: str,
    auto_enter: bool,
    exit_code: bool,
) -> None:
    """
    Confirmation prompt.
    """
    k = object() if key is None else object()
    assert_unique_key(k, ctx)
    ctx.questions[k] = q.confirm(
        message=prompt,
        default=default,
        instruction=f'{instruction or ("(Y/n)" if default else "(y/N)")}: ',
        auto_enter=auto_enter,
    )
    if exit_code:
        ctx.confirm_exit_nonzero.add(k)


@command()
@option_prompt()
@option_key()
@option_choices()
@option_default()
@option_instruction()
@pass_context
def select(
    ctx: Context,
    prompt: str,
    key: str,
    choices: str,
    default: str | None,
    instruction: str,
) -> None:
    """
    Select option prompt.
    """
    assert_unique_key(key, ctx)
    try:
        items = json.loads(choices)
        if not isinstance(items, list):
            raise TypeError
    except Exception as exc:
        raise click.UsageError('Choices must be a valid JSON list of strings.') from exc
    if not items:
        raise click.UsageError('At least one choice is required.')

    if default and default not in items:
        raise click.UsageError('Default value must be one of the choices.')

    ctx.questions[key] = q.select(
        message=prompt,
        choices=items,
        default=default,
        instruction=f'{instruction}: ' if instruction else '',
    )


@command()
@option_prompt()
@option_key()
@pass_context
def rawselect(
    ctx: Context,
    prompt: str,
    key: str,
) -> None:
    """
    Raw select option prompt.
    """
    assert_unique_key(key, ctx)
    raise NotImplementedError  # todo


@command()
@option_prompt()
@option_key()
@pass_context
def checkbox(
    ctx: Context,
    prompt: str,
    key: str,
) -> None:
    """
    Multi-select checkbox prompt.
    """
    assert_unique_key(key, ctx)
    raise NotImplementedError  # todo


@command()
@option_prompt()
@option_key()
@pass_context
def autocomplete(
    ctx: Context,
    prompt: str,
    key: str,
) -> None:
    """
    Autocomplete text prompt.
    """
    assert_unique_key(key, ctx)
    raise NotImplementedError  # todo


@command()
@click.option(
    '-t',
    '--text',
    help='Text to be printed.',
    required=True,
)
@pass_context
def print(
    ctx: Context,
    text: str,
) -> None:
    """
    Print formatted text.
    """
    ctx.questions[object()] = PrintQuestionAdapter(text=text)  # type: ignore


@command()
@option_prompt(default='Press any key to continue...')
@click.option(
    '-a',
    '--append',
    is_flag=True,
    default=False,
    help='When option is set, append " press any key to continue..." to the prompt.',
)
@pass_context
def wait(
    ctx: Context,
    prompt: str,
    append: bool,
) -> None:
    """
    Wait until any key is pressed.
    """
    q.press_any_key_to_continue(
        message=prompt + (' press any key to continue...' if append else '')
    ).ask()


@cli.result_callback()
@pass_context
def process(ctx: Context, *args: Any, **kwargs: Any) -> None:
    # process
    answers = {}
    exit_code = 0
    for key, question in ctx.questions.items():
        answers[key] = question.ask()
        if key in ctx.confirm_exit_nonzero and answers[key] is False:
            exit_code = 1
            break
    # drop non-keys
    answers = {k: v for k, v in answers.items() if isinstance(k, str)}
    # output
    if isinstance(ctx.file, str):
        fp = Path(ctx.file)
        fp.parent.mkdir(parents=True, exist_ok=True)
        stream = fp.open('wt')
    else:
        stream = ctx.file  # type: ignore[assignment]
    with stream as f:
        if ctx.output is OutputType.JSON:
            f.write(json.dumps(answers))
        elif ctx.output is OutputType.PLAIN:
            f.write('\n'.join(f'{k}={v}' for k, v in answers.items()))
    # exit
    sys.exit(exit_code)


# Helpers


class Usage(Exception): ...


class PrintQuestionAdapter:
    def __init__(self, text: str) -> None:
        self.text = text

    def ask(self) -> None:
        q.print(text=self.text)


def process_help(arg: object) -> None:
    if arg in ('--help', '-h'):
        raise Usage


def assert_unique_key(key: Key, ctx: Context) -> None:
    process_help(key)
    if key in ctx.questions:
        raise click.UsageError(f'Question key "{key}" is already used.')
