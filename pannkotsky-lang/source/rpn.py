from typing import List

from shortuuid import ShortUUID


def generate_label_name():
    return f'_label_{ShortUUID().random(length=10)}'


def _get_next_index(index, tokens_map):
    max_index = max(tokens_map.keys())
    if index >= max_index:
        raise KeyError

    try:
        tokens_map[index + 1]
    except KeyError:
        return _get_next_index(index + 1, tokens_map)
    else:
        return index + 1


class RPNBuilder:
    _PRIORITIES = {
        '(': 0,
        'if': 0,
        'repeat': 0,
        ')': 1,
        'until': 1,
        '\\n': 1,
        'print': 2,
        'goto': 2,
        'label': 2,
        ':=': 2,
        'var': 3,
        '<': 4,
        '>': 4,
        '<=': 4,
        '>=': 4,
        '==': 4,
        '!=': 4,
        '+': 5,
        '-': 5,
        '*': 6,
        '/': 6,
        '^': 7,
    }

    def __init__(self, tokens: List[str]):
        self._tokens = tokens
        self._stack = []
        self._output = []

    def build(self):
        """
        Process input tokens in infix form to postfix form according to Dijkstra algorithm.
        """

        for token in self._tokens:
            priority = self._PRIORITIES.get(token)

            # token is operand
            if priority is None:
                self._output.append(token)
                continue

            if token == '(':
                self._to_stack(token)
                continue

            if token == '\\n' and self._stack[-1] == '\\n' and 'if' in self._stack:
                # double '\\n' acts as end of 'if' operation
                assert self._stack.pop() == '\\n'
                while self._stack and self._stack[-1] != 'if':
                    assert self._stack[-1].startswith('_label_')
                    self._output.append(self._stack.pop())
                assert self._stack.pop() == 'if'
                self._output.append('label')
                self._to_stack(token)
                continue

            if token == '\\n' and 'until' in self._stack:
                while self._stack[-1] != 'until':
                    self._output.append(self._stack.pop())
                assert self._stack.pop() == 'until'
                assert self._stack[-1].startswith('_label_')
                self._output.append(self._stack.pop())
                assert self._stack.pop() == 'repeat'
                self._output.append('goto_if_not')
                self._to_stack(token)
                continue

            # the only thing which can be in stack and not in self._PRIORITIES is label
            # giving it priority -1 (it can be pushed out of stack by special case only)
            while self._stack and self._PRIORITIES.get(self._stack[-1], -1) >= priority:
                self._stack_to_output()

            # either stack is empty or last operation priority is lower
            self._to_stack(token)

        # input is empty
        while self._stack:
            self._stack_to_output()

        return self._replace_labels(self._output)

    def _to_stack(self, token: str):
        if self._stack and self._stack[-1] == '\\n':
            self._stack.pop()

        if token == 'repeat':
            label = generate_label_name()
            self._stack.append(token)
            self._stack.append(label)
            self._output.append(label)
            self._output.append('label')

        elif token == '\\n' and self._stack:
            if self._stack[-1] == 'if':
                # '\\n' acts as 'then' in this case
                label = generate_label_name()
                self._stack.append(label)
                self._output.append(label)
                self._output.append('goto_if_not')
            else:
                self._stack.append(token)

        elif token == ')':
            # pop the '(' out of stack
            assert self._stack.pop() == '('
        else:
            self._stack.append(token)

    def _stack_to_output(self):
        stack_token = self._stack.pop()
        assert stack_token not in ['(', 'if']
        assert not stack_token.startswith('_label_')

        if stack_token != '\\n':
            self._output.append(stack_token)

    @staticmethod
    def _replace_labels(tokens: List[str]):
        """ Replace labels with tokens address. """

        tokens_with_indexes = list(zip(range(len(tokens)), tokens))
        tokens_map = dict(tokens_with_indexes)
        labels_map = {}
        for index, token in tokens_with_indexes[::-1]:
            if token == 'label':
                labels_map[tokens[index - 1]] = _get_next_index(index, tokens_map)
                del tokens_map[index]
                del tokens_map[index - 1]

        indexes_list = sorted(tokens_map.keys())
        for label, value in labels_map.items():
            labels_map[label] = str(indexes_list.index(value))

        for index, token in tokens_map.items():
            if token in labels_map:
                tokens_map[index] = labels_map[token]

        return [tokens_map[index] for index in indexes_list]
