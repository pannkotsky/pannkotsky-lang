from typing import List

from shortuuid import ShortUUID


def generate_label_name():
    return f'_label_{ShortUUID().random(length=10)}'


class RPNBuilder:
    PRIORITIES = {
        '(': 0,
        'if': 0,
        ')': 1,
        '\n': 1,
        'print': 2,
        'goto': 2,
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
        self.tokens = tokens
        self.stack = []
        self.output = []

    def to_stack(self, token: str):
        if self.stack and self.stack[-1] == '\n':
            self.stack.pop()

        if token == '\n' and self.stack:
            if self.stack[-1] == 'if':
                # '\n' acts as 'then' in this case
                label = generate_label_name()
                self.stack.append(label)
                self.output.append(label)
                self.output.append('goto_if_not')
            else:
                self.stack.append(token)

        elif token == ')':
            # pop the '(' out of stack
            assert self.stack.pop() == '('
        else:
            self.stack.append(token)

    def stack_to_output(self):
        stack_token = self.stack.pop()
        assert stack_token not in ['(', 'if']
        assert not stack_token.startswith('_label_')

        if stack_token != '\n':
            self.output.append(stack_token)

    def build(self):
        """
        Process input tokens in infix form to postfix form according to Dijkstra algorithm.
        """

        for token in self.tokens:
            priority = self.PRIORITIES.get(token)

            # token is operand
            if priority is None:
                self.output.append(token)
                continue

            if token == '(':
                self.to_stack(token)
                continue

            if token == '\n' and self.stack[-1] == '\n' and 'if' in self.stack:
                # double '\n' acts as end of 'if' operation
                assert self.stack.pop() == '\n'
                while self.stack and self.stack[-1] != 'if':
                    assert self.stack[-1].startswith('_label_')
                    self.output.append(self.stack.pop())
                assert self.stack.pop() == 'if'
                self.output.append('label')
                self.to_stack(token)
                continue

            # the only thing which can be in stack and not in self.PRIORITIES is label
            # giving it priority -1 (it can be pushed out of stack by special case only)
            while self.stack and self.PRIORITIES.get(self.stack[-1], -1) >= priority:
                self.stack_to_output()

            # either stack is empty or last operation priority is lower
            self.to_stack(token)

        # input is empty
        while self.stack:
            self.stack_to_output()

        return self.output
