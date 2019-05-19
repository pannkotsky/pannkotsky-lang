from inspect import getfullargspec
from typing import List


class Jump(Exception):
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
        'goto_if_not': '_goto_if_not',
    }

    def __init__(self, tokens: List[str]):
        self._tokens = self._prepare(tokens)
        self._indexes_list = sorted(self._tokens.keys())
        self._current_token_index = self._indexes_list[0]
        self._idents_registry = {}

    @property
    def tokens(self):
        return self._tokens

    def execute(self):
        execution_stack = []

        while True:
            try:
                token = self._tokens[self._current_token_index]
            except KeyError:
                break
            execution_stack.append(token)

            if token in self.OPERATIONS_MAP:
                # in case of operation extract the amount of arguments it requires
                # and perform operation
                operation, args = self._get_operation(execution_stack)
                try:
                    res = operation(*args)
                except Jump:
                    continue

                # if operation returns some result put it back to stack
                if res is not None:
                    execution_stack.append(res)

            try:
                self._current_token_index = self._get_next_index()
            except IndexError:
                break

    @staticmethod
    def _prepare(tokens: List[str]):
        """ Create dict instead of list, replace labels with tokens address. """

        tokens_with_indexes = list(zip(range(len(tokens)), tokens))
        tokens_map = dict(tokens_with_indexes)
        labels_map = {}
        for index, token in tokens_with_indexes:
            if token == 'label':
                assert tokens[index - 1].startswith('_label_')
                labels_map[tokens[index - 1]] = index + 1
                del tokens_map[index]
                del tokens_map[index - 1]

        for index, token in tokens_map.items():
            if token.startswith('_label_'):
                tokens_map[index] = labels_map[token]

        return tokens_map

    def _get_operation(self, execution_stack: List):
        """ Returns method by operation name and args it requires. """

        operation_name = self.OPERATIONS_MAP[execution_stack.pop()]
        operation = getattr(self, operation_name)
        signature = getfullargspec(operation)
        numargs = len(signature.args) - 1  # exclude 'self' arg

        assert len(execution_stack) >= numargs

        args = []
        for _ in range(numargs):
            args = [execution_stack.pop()] + args

        return operation, args

    def _get_value(self, arg, target_type=None):
        if arg in self._idents_registry:
            return self._idents_registry[arg]
        return self._cast_value(arg, target_type)

    @staticmethod
    def _cast_value(value, target_type=None):
        if target_type is not None:
            return target_type(value)

        # if we support more types in future, add type autodetection
        return int(value)

    def _get_next_index(self):
        return self._indexes_list[self._indexes_list.index(self._current_token_index) + 1]

    ############### Operations ###############

    def _goto(self, token_index: int):
        assert isinstance(token_index, int)
        self._current_token_index = token_index
        raise Jump

    def _goto_if_not(self, condition: bool, token_index: int):
        assert isinstance(condition, bool)
        if not condition:
            self._goto(token_index)

    def _declare_ident(self, ident: str) -> str:
        self._idents_registry[ident] = None
        return ident

    def _assign(self, ident: str, value) -> str:
        self._idents_registry[ident] = self._get_value(value)
        return ident

    def _print(self, arg):
        print(self._get_value(arg))

    def _add(self, v1, v2):
        return self._get_value(v1, int) + self._get_value(v2, int)

    def _subtract(self, v1, v2):
        return self._get_value(v1, int) - self._get_value(v2, int)

    def _multiply(self, v1, v2):
        return self._get_value(v1, int) * self._get_value(v2, int)

    def _divide(self, v1, v2):
        return self._get_value(v1, int) // self._get_value(v2, int)

    def _to_power(self, value, power):
        return self._get_value(value, int) ** self._get_value(power)

    def _lt(self, v1, v2) -> bool:
        return self._get_value(v1, int) < self._get_value(v2, int)

    def _lte(self, v1, v2) -> bool:
        return self._get_value(v1, int) <= self._get_value(v2, int)

    def _gt(self, v1, v2) -> bool:
        return self._get_value(v1, int) > self._get_value(v2, int)

    def _gte(self, v1, v2) -> bool:
        return self._get_value(v1, int) >= self._get_value(v2, int)

    def _eq(self, v1, v2) -> bool:
        return self._get_value(v1, int) == self._get_value(v2, int)

    def _ne(self, v1, v2) -> bool:
        return self._get_value(v1, int) != self._get_value(v2, int)
