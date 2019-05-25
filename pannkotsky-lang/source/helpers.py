from .alphabet import ALPHABET, LETTERS, DIGITS
from .rpn import RPNBuilder
from .scan import Scanner
from .tokens import tokens, tokens_map


def is_symbol(symbol):
    return symbol in ALPHABET


def is_letter(symbol):
    return symbol in LETTERS


def is_digit(symbol):
    return symbol in DIGITS


def get_language_tokens_table():
    headers = ['Token', 'Id', 'Description']
    rows = []
    for token_args in tokens:
        token = token_args[0]
        token_obj = tokens_map[token]
        rows.append([token_obj.representation, token_obj.id, token_obj.description])
    return {
        'headers': headers,
        'rows': rows,
    }


def get_scan_output_table(scanner: Scanner):
    return {
        'headers': ['Numline', 'Numchar', 'Char', 'State', 'Token'],
        'rows': scanner.output,
    }


def get_program_tokens_table(scanner: Scanner):
    headers = ['Line no', 'Token', 'Id', 'Ident/Const id']
    rows = [scan_token.to_table_row() for scan_token in scanner.scan_tokens]
    return {
        'headers': headers,
        'rows': rows,
    }


def get_idents_table(scanner: Scanner):
    return {
        'headers': ['Ident', 'Id'],
        'rows': scanner.idents_map.items(),
    }


def get_contants_table(scanner: Scanner):
    return {
        'headers': ['Const', 'Id'],
        'rows': scanner.constants_map.items(),
    }


def get_labels_table(scanner: Scanner):
    return {
        'headers': ['Label', 'Id'],
        'rows': scanner.labels_map.items(),
    }


def get_rpn_table(rpn_builder: RPNBuilder):
    return {
        'headers': ['Input symbol', 'Stack', 'Output'],
        'rows': rpn_builder.rpn_steps
    }
