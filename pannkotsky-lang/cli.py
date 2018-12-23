#!/usr/bin/env python3
import os
import time

import click
from tabulate import tabulate

from source.scan import Scanner
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
    output_fname = input_file.name.rsplit('/', 1)[-1]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'outputs', f'{output_fname}_{time.time()}.csv')
    with open(output_path, 'w') as output_file:
        scanner = Scanner(input_file, output_file)
        scanner.scan()

    click.echo("Program tokens table")
    headers = ['Line no', 'Token', 'Id', 'Ident/Const id']
    click.echo(tabulate(scanner.scan_tokens, headers, 'grid'))

    click.echo("\nIdentifiers table")
    headers = ['Ident', 'Id']
    click.echo(tabulate(scanner.idents_map.items(), headers, 'grid'))

    click.echo("\nConstants table")
    headers = ['Const', 'Id']
    click.echo(tabulate(scanner.constants_map.items(), headers, 'grid'))

    click.echo("\nLabels table")
    headers = ['Label', 'Id']
    click.echo(tabulate(scanner.labels_map.items(), headers, 'grid'))


if __name__ == '__main__':
    cli()
