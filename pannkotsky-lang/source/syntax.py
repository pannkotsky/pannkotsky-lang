from typing import Iterable, List

from .errors import PKLSyntaxError
from .tokens import ScanToken

ScanTokens = List[ScanToken]


class NotEnoughTokens(Exception):
    pass


class SyntaxAnalyzer:
    def __init__(self, tokens: ScanTokens):
        self._input_tokens = tokens

    def run(self):
        tokens = self._input_tokens
        # no tokens is a valid program
        if not tokens:
            return
        total_processed = 0
        while total_processed < len(tokens):
            try:
                total_processed += self.block(tokens[total_processed:])
            except NotEnoughTokens:
                raise PKLSyntaxError('Unexpected end of program', tokens[-1].numline)
        return [token.token_repr for token in tokens]

    def check_token(self, tokens: ScanTokens, expected: Iterable[str]):
        if not tokens:
            raise NotEnoughTokens

        token_str = tokens[0].get_token_str()
        if token_str not in expected:
            raise PKLSyntaxError(f'{expected} expected, got {token_str}', tokens[0].numline)
        return 1

    def block(self, tokens: ScanTokens) -> int:
        total_processed = self.statement(tokens)
        while total_processed < len(tokens):
            # empty line separates block
            try:
                self.separator(tokens[total_processed:])
            except PKLSyntaxError:
                pass
            else:
                return total_processed
            try:
                total_processed += self.statement(tokens[total_processed:])
            except PKLSyntaxError:
                break
        return total_processed

    def statement(self, tokens: ScanTokens) -> int:
        for method in [
            self.assignment,
            self.loop,
            self.condition,
            self.goto,
            self.label,
            self.output
        ]:
            total_processed = method(tokens)
            if total_processed > 0:
                break
        total_processed += self.separator(tokens[total_processed:])
        return total_processed

    def separator(self, tokens: ScanTokens) -> int:
        return self.check_token(tokens, ['\n'])

    def assignment(self, tokens: ScanTokens) -> int:
        total_processed = 0
        var_found = False
        try:
            total_processed += self.check_token(tokens[total_processed:], ['var'])
        except (PKLSyntaxError, NotEnoughTokens):
            pass
        else:
            var_found = True
        try:
            total_processed += self.check_token(tokens[total_processed:], ['_IDENT'])
        except (PKLSyntaxError, NotEnoughTokens):
            if var_found:
                raise
            return total_processed
        total_processed += self.check_token(tokens[total_processed:], [':='])
        total_processed += self.expression(tokens[total_processed:])
        return total_processed

    def expression(self, tokens: ScanTokens) -> int:
        total_processed = 0
        try:
            total_processed += self.check_token(tokens, ['('])
        except PKLSyntaxError:
            total_processed += self.operand(tokens[total_processed:])
        else:
            total_processed += self.expression(tokens[total_processed:])
            total_processed += self.check_token(tokens[total_processed:], [')'])

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
        try:
            total_processed += self.check_token(tokens[total_processed:], ['repeat'])
        except (PKLSyntaxError, NotEnoughTokens):
            return total_processed
        total_processed += self.separator(tokens[total_processed:])
        total_processed += self.block(tokens[total_processed:])
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
        try:
            total_processed += self.check_token(tokens[total_processed:], ['if'])
        except (PKLSyntaxError, NotEnoughTokens):
            return total_processed
        total_processed += self.logical_expression(tokens[total_processed:])
        total_processed += self.separator(tokens[total_processed:])
        total_processed += self.block(tokens[total_processed:])
        return total_processed

    def goto(self, tokens: ScanTokens) -> int:
        total_processed = 0
        try:
            total_processed += self.check_token(tokens[total_processed:], ['goto'])
        except (PKLSyntaxError, NotEnoughTokens):
            return total_processed
        total_processed += self.check_token(tokens[total_processed:], ['_LABEL'])
        return total_processed

    def label(self, tokens: ScanTokens) -> int:
        total_processed = 0
        try:
            total_processed += self.check_token(tokens[total_processed:], ['label'])
        except (PKLSyntaxError, NotEnoughTokens):
            return total_processed
        total_processed += self.check_token(tokens[total_processed:], ['_LABEL'])
        return total_processed

    def output(self, tokens: ScanTokens) -> int:
        total_processed = 0
        try:
            total_processed += self.check_token(tokens[total_processed:], ['print'])
        except (PKLSyntaxError, NotEnoughTokens):
            return total_processed
        total_processed += self.expression(tokens[total_processed:])
        return total_processed
