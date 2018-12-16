#!/usr/bin/env python3


class Token:
    def __init__(self, id, token, description, representation=None):
        self.id = id
        self.token = token
        self.description = description
        self.representation = representation or token

    def __str__(self):
        return self.token


tokens = [
    (':=', 'assignment'),
    ('+', 'addition'),
    ('-', 'subtraction'),
    ('*', 'multiplication'),
    ('/', 'division'),
    ('^', 'power'),
    ('(', 'opening bracket'),
    (')', 'closing bracket'),
    ('<', 'less than'),
    ('>', 'more than'),
    ('<=', 'less than or equal to'),
    ('>=', 'more than or equal to'),
    ('==', 'equal to'),
    ('var', 'variable declaration'),
    ('\n', 'newline', '\\n'),
    ('repeat', 'loop operators block start'),
    ('until', 'loop condition start'),
    ('if', 'condition start'),
    ('goto', 'goto statement'),
    ('label', 'label for goto'),
    ('print', 'output operator'),
    ('_IDENT', 'ident'),
    ('_CONST', 'const'),
]

tokens_id_map = {}
tokens_map = {}
for index, args in enumerate(tokens):
    token = Token(index, *args)
    tokens_id_map[index] = token
    tokens_map[args[0]] = token


def main():
    from tabulate import tabulate
    headers = ['Token', 'Id', 'Description']
    table = []
    for token_args in tokens:
        token = token_args[0]
        token_obj = tokens_map[token]
        table.append([token_obj.representation, token_obj.id, token_obj.description])
    print(tabulate(table, headers, tablefmt='grid'))


if __name__ == '__main__':
    main()


"""
+---------+------+----------------------------+
| Token   |   Id | Description                |
+=========+======+============================+
| :=      |    0 | assignment                 |
+---------+------+----------------------------+
| +       |    1 | addition                   |
+---------+------+----------------------------+
| -       |    2 | subtraction                |
+---------+------+----------------------------+
| *       |    3 | multiplication             |
+---------+------+----------------------------+
| /       |    4 | division                   |
+---------+------+----------------------------+
| ^       |    5 | power                      |
+---------+------+----------------------------+
| (       |    6 | opening bracket            |
+---------+------+----------------------------+
| )       |    7 | closing bracket            |
+---------+------+----------------------------+
| <       |    8 | less than                  |
+---------+------+----------------------------+
| >       |    9 | more than                  |
+---------+------+----------------------------+
| <=      |   10 | less than or equal to      |
+---------+------+----------------------------+
| >=      |   11 | more than or equal to      |
+---------+------+----------------------------+
| ==      |   12 | equal to                   |
+---------+------+----------------------------+
| var     |   13 | variable declaration       |
+---------+------+----------------------------+
| \n      |   14 | newline                    |
+---------+------+----------------------------+
| repeat  |   15 | loop operators block start |
+---------+------+----------------------------+
| until   |   16 | loop condition start       |
+---------+------+----------------------------+
| if      |   17 | condition start            |
+---------+------+----------------------------+
| goto    |   18 | goto statement             |
+---------+------+----------------------------+
| label   |   19 | label for goto             |
+---------+------+----------------------------+
| print   |   20 | output operator            |
+---------+------+----------------------------+
| _IDENT  |   21 | ident                      |
+---------+------+----------------------------+
| _CONST  |   22 | const                      |
+---------+------+----------------------------+
"""
