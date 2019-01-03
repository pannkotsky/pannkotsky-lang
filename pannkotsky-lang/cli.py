#!/usr/bin/env python3
import click
from tabulate import tabulate

from source.scan import Scanner
from source.syntax import SyntaxAnalyzer
from source.tokens import tokens, tokens_map


@click.group()
def cli():
    pass


@cli.command()
def tokens_list():
    headers = ['Token', 'Id', 'Description']
    table = []
    for token_args in tokens:
        token = token_args[0]
        token_obj = tokens_map[token]
        table.append([token_obj.representation, token_obj.id, token_obj.description])
    click.echo(tabulate(table, headers, tablefmt='grid'))


@cli.command()
@click.argument('input_file', type=click.File('r'))
def scan(input_file):
    scanner = Scanner(input_file)
    scanner.scan()

    click.echo("Analysis table")
    headers = ['Numline', 'Numchar', 'Char', 'State', 'Token']
    click.echo(tabulate(scanner.output, headers, 'grid'))

    click.echo("\nProgram tokens table")
    headers = ['Line no', 'Token', 'Id', 'Ident/Const id']
    rows = [scan_token.to_table_row() for scan_token in scanner.scan_tokens]
    click.echo(tabulate(rows, headers, 'grid'))

    click.echo("\nIdentifiers table")
    headers = ['Ident', 'Id']
    click.echo(tabulate(scanner.idents_map.items(), headers, 'grid'))

    click.echo("\nConstants table")
    headers = ['Const', 'Id']
    click.echo(tabulate(scanner.constants_map.items(), headers, 'grid'))

    click.echo("\nLabels table")
    headers = ['Label', 'Id']
    click.echo(tabulate(scanner.labels_map.items(), headers, 'grid'))


@cli.command()
@click.argument('input_file', type=click.File('r'))
def syntax_check(input_file):
    scanner = Scanner(input_file)
    scanner.scan()

    syntax_analyzer = SyntaxAnalyzer(scanner.scan_tokens)
    syntax_analyzer.run()

    click.echo("Syntax check successful")


if __name__ == '__main__':
    cli()
