# TODO: rewrite this file so it assumes a flat list of tokens from RPNBuilder

from inspect import getfullargspec
from typing import List

from .tokens import ScanToken

ScanTokens = List[ScanToken]


class ExpressionTermination(Exception):
    """ Expression is terminated on goto instruction. """
    pass


class BlockTermination(Exception):
    """ This means there are no more expressions to process or goto led to not existing label. """
    pass


class Executor:
    OPERATIONS_MAP = {
        ':=': '_assign',
        '+': '_add',
        '-': '_subtract',
        '*': '_multiply',
        '/': '_divide',
        '^': '_to_power',
        '<': '_lt',
        '>': '_gt',
        '<=': '_lte',
        '>=': '_gte',
        '==': '_eq',
        '!=': '_ne',
        'var': '_declare_ident',
        'print': '_print',
        'label': '_declare_label',
        'goto': '_goto',
    }

    def __init__(self, expressions, parent=None):
        self.expressions = expressions
        self.parent = parent
        self.idents_registry = {}
        self.labels_registry = {}
        self.current_expr_index = 0

    def execute(self):
        while True:
            try:
                self.execute_expression()
            except ExpressionTermination:
                continue
            except BlockTermination:
                break
            else:
                self.next()

    def execute_expression(self):
        expression = self.current_expression()

        if not expression:
            return

        execution_stack = []

        for token in expression:
            if isinstance(token, list):
                executor = Executor(token, parent=self)
                executor.execute()
                continue

            execution_stack.append(token)

            # go to the next token in case of operand
            if token not in self.OPERATIONS_MAP:
                continue

            # in case of operation extract the amount of arguments it requires and perform
            operation, args = self.get_operation(execution_stack)
            res = operation(*args)

            # if operation returns some result put it back to stack
            if res is not None:
                execution_stack.append(res)

    def get_operation(self, execution_stack: ScanTokens):
        """ Returns method by operation name and args it requires. """
        operation_name = self.OPERATIONS_MAP[execution_stack.pop().token_repr]
        operation = getattr(self, operation_name)
        signature = getfullargspec(operation)
        numargs = len(signature['args']) - 1  # exclude 'self' arg
        args = []
        for _ in range(numargs):
            args = [execution_stack.pop()] + args

        args = [self.get_value(arg) for arg in args]

        return operation, args

    def get_value(self, ident: ScanToken):
        token = ident.get_token_str()

        if token == '_IDENT':
            return self.get_ident_value(ident.token_repr)

        if token == '_LABEL':
            return self.get_label_value(ident.token_repr)

        return ident.token_repr

    def current_expression(self):
        try:
            return self.expressions[self.current_expr_index]
        except IndexError:
            raise BlockTermination

    def next(self):
        self.current_expr_index += 1

    def get_ident_value(self, ident: str):
        try:
            return self.idents_registry[ident]
        except KeyError:
            # there must be parent with the ident
            assert self.parent is not None
            return self.parent.get_ident_value(ident)

    def get_label_value(self, label: str):
        return self.labels_registry[label]

    ############### Operations ###############

    def _goto(self, expr_index: int):
        self.current_expr_index = expr_index
        raise ExpressionTermination

    def _goto_if_not(self, label: str, condition: bool):
        if not condition:
            self._goto(label)

    def _declare_ident(self, ident: str):
        self.idents_registry[ident] = None

    def _assign(self, ident: str, value):
        self.idents_registry[ident] = value

    def _declare_label(self, label: str):
        self.labels_registry[label] = self.current_expr_index + 1

    def _print(self, arg):
        print(arg)

    def _add(self, value1, value2):
        return value1 + value2

    def _subtract(self, value1, value2):
        return value1 - value2

    def _multiply(self, value1, value2):
        return value1 * value2

    def _divide(self, value1, value2):
        return value1 / value2

    def _to_power(self, value, power):
        return value ** power

    def _lt(self, value1, value2):
        return value1 < value2

    def _lte(self, value1, value2):
        return value1 <= value2

    def _gt(self, value1, value2):
        return value1 > value2

    def _gte(self, value1, value2):
        return value1 >= value2

    def _eq(self, value1, value2):
        return value1 == value2

    def _ne(self, value1, value2):
        return value1 != value2
