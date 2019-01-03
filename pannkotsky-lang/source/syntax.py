from typing import Iterable, List

from .errors import PKLSyntaxError
from .scan import ScanToken

ScanTokens = List[ScanToken]


class NotEnoughTokens(Exception):
    pass


class SyntaxAnalyzer:
    def __init__(self, tokens: ScanTokens):
        self.tokens = tokens

    def run(self):
        tokens = self.tokens
        # no tokens is a valid program
        if not tokens:
            return
        try:
            processed = self.block(tokens)
        except NotEnoughTokens:
            raise PKLSyntaxError('Unexpected end of program', tokens[-1].numline)
        if processed < len(tokens):
            raise PKLSyntaxError('Statements block expected', tokens[processed].numline)

    def check_token(self, tokens: ScanTokens, expected: Iterable[str]):
        if not tokens:
            raise NotEnoughTokens

        token_str = tokens[0].get_token_str()
        if token_str not in expected:
            raise PKLSyntaxError(f'{expected} expected, got {token_str}', tokens[0].numline)
        return 1

    def block(self, tokens: ScanTokens) -> int:
        total_processed = self.statement(tokens)
        tokens = tokens[total_processed:]
        while tokens:
            try:
                total_processed += self.statement(tokens)
            except PKLSyntaxError:
                pass
            else:
                tokens = tokens[total_processed:]
        return total_processed

    def statement(self, tokens: ScanTokens) -> int:
        total_processed = 0
        for method in [
            self.assignment,
            self.loop,
            self.condition,
            self.goto,
            self.label,
            self.output
        ]:
            try:
                total_processed = method(tokens)
            except (PKLSyntaxError, NotEnoughTokens):
                pass
            else:
                break
        total_processed += self.separator(tokens[total_processed:])
        return total_processed

    def separator(self, tokens: ScanTokens) -> int:
        return self.check_token(tokens, '\n')

    def assignment(self, tokens: ScanTokens) -> int:
        total_processed = 0
        total_processed += self.check_token(tokens[total_processed:], ['var'])
        total_processed += self.check_token(tokens[total_processed:], ['_IDENT'])
        total_processed += self.check_token(tokens[total_processed:], [':='])
        total_processed += self.expression(tokens[total_processed:])
        return total_processed

    def expression(self, tokens: ScanTokens) -> int:
        total_processed = 0
        try:
            total_processed += self.check_token(tokens, ['('])
        except PKLSyntaxError:
            pass
        else:
            total_processed += self.expression(tokens[total_processed:])
            total_processed += self.check_token(tokens[total_processed:], [')'])
            return total_processed

        total_processed += self.operand(tokens[total_processed:])

        try:
            total_processed += self.operation(tokens[total_processed:])
        except (PKLSyntaxError, NotEnoughTokens):
            return total_processed

        total_processed += self.expression(tokens[total_processed:])
        return total_processed

    def operand(self, tokens: ScanTokens) -> int:
        return self.check_token(tokens, ['_IDENT', '_CONST'])

    def operation(self, tokens: ScanTokens) -> int:
        return self.check_token(tokens, ['+', '-', '*', '/', '^'])

    def loop(self, tokens: ScanTokens) -> int:
        total_processed = 0
        total_processed += self.check_token(tokens[total_processed:], ['repeat'])
        total_processed += self.separator(tokens[total_processed:])
        total_processed += self.block(tokens[total_processed:])
        total_processed += self.separator(tokens[total_processed:])
        total_processed += self.check_token(tokens[total_processed:], ['until'])
        total_processed += self.logical_expression(tokens[total_processed:])
        return total_processed

    def logical_expression(self, tokens: ScanTokens) -> int:
        total_processed = 0
        total_processed += self.expression(tokens[total_processed:])
        total_processed += self.logical_operation(tokens[total_processed:])
        total_processed += self.expression(tokens[total_processed:])
        return total_processed

    def logical_operation(self, tokens: ScanTokens) -> int:
        return self.check_token(tokens, ['<', '>', '<=', '>=', '=='])

    def condition(self, tokens: ScanTokens) -> int:
        total_processed = 0
        total_processed += self.check_token(tokens[total_processed:], ['if'])
        total_processed += self.logical_expression(tokens[total_processed:])
        total_processed += self.separator(tokens[total_processed:])
        total_processed += self.block(tokens[total_processed:])
        return total_processed

    def goto(self, tokens: ScanTokens) -> int:
        total_processed = 0
        total_processed += self.check_token(tokens[total_processed:], ['goto'])
        total_processed += self.check_token(tokens[total_processed:], ['_LABEL'])
        return total_processed

    def label(self, tokens: ScanTokens) -> int:
        total_processed = 0
        total_processed += self.check_token(tokens[total_processed:], ['label'])
        total_processed += self.check_token(tokens[total_processed:], ['_LABEL'])
        return total_processed

    def output(self, tokens: ScanTokens) -> int:
        total_processed = 0
        total_processed += self.check_token(tokens[total_processed:], ['print'])
        total_processed += self.expression(tokens[total_processed:])
        return total_processed
