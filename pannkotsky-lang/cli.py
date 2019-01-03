#!/usr/bin/env python3
import click
from tabulate import tabulate

from source.helpers import (get_language_tokens_table, get_scan_output_table,
                            get_program_tokens_table, get_idents_table, get_contants_table,
                            get_labels_table)
from source.scan import Scanner
from source.syntax import SyntaxAnalyzer


def _print_table(table):
    click.echo(tabulate(table['rows'], table['headers'], 'grid'))


def _scan(input_file):
    scanner = Scanner(input_file)
    scanner.scan()

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

    return scanner


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
    scanner = _scan(input_file)

    click.echo('\n')

    syntax_analyzer = SyntaxAnalyzer(scanner.scan_tokens)
    syntax_analyzer.run()

    click.echo("Syntax check successful")


if __name__ == '__main__':
    cli()
