#!/usr/bin/env python3
import click
from tabulate import tabulate

from source.helpers import (get_language_tokens_table, get_scan_output_table,
                            get_program_tokens_table, get_idents_table, get_contants_table,
                            get_labels_table, get_rpn_table)
from source.errors import PKLanguageError
from source.scan import Scanner
from source.syntax import SyntaxAnalyzer
from source.rpn import RPNBuilder
from source.exec import Executor


def _print_table(table):
    click.echo(tabulate(table['rows'], table['headers'], 'grid'))


def _scan(input_file):
    scanner = Scanner(input_file)

    try:
        tokens = scanner.scan()
    except PKLanguageError as e:
        click.echo(str(e))
        exit(1)
        return

    click.echo("Analysis table")
    _print_table(get_scan_output_table(scanner))

    click.echo("\nProgram tokens table")
    _print_table(get_program_tokens_table(scanner))

    click.echo("\nIdentifiers table")
    _print_table(get_idents_table(scanner))

    click.echo("\nConstants table")
    _print_table(get_contants_table(scanner))

    click.echo("\nLabels table")
    _print_table(get_labels_table(scanner))

    return tokens


def _syntax_check(input_file):
    scan_tokens = _scan(input_file)

    click.echo('\n')

    try:
        syntax_tokens = SyntaxAnalyzer(scan_tokens).run()
    except PKLanguageError as e:
        click.echo(str(e))
        exit(1)
        return

    click.echo("Syntax check successful")

    return syntax_tokens


def _rpn(input_file):
    syntax_tokens = _syntax_check(input_file)

    rpn_builder = RPNBuilder(syntax_tokens)
    rpn_tokens = rpn_builder.build()

    click.echo('\nRPN steps table')
    _print_table(get_rpn_table(rpn_builder))

    click.echo('\nResulting RPN')
    click.echo(rpn_tokens)

    return rpn_tokens


def _execute(input_file):
    rpn_tokens = _rpn(input_file)

    executor = Executor(rpn_tokens)

    click.echo('\n')
    click.echo('Executor output')

    executor.execute()


@click.group()
def cli():
    pass


@cli.command()
def tokens_list():
    _print_table(get_language_tokens_table())


@cli.command()
@click.argument('input_file', type=click.File('r'))
def scan(input_file):
    _scan(input_file)


@cli.command()
@click.argument('input_file', type=click.File('r'))
def syntax_check(input_file):
    _syntax_check(input_file)


@cli.command()
@click.argument('input_file', type=click.File('r'))
def rpn(input_file):
    _rpn(input_file)


@cli.command()
@click.argument('input_file', type=click.File('r'))
def execute(input_file):
    _execute(input_file)


if __name__ == '__main__':
    cli()
