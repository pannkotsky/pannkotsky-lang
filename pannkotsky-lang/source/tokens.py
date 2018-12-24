class Token:
    def __init__(self, id: int, token: str, description: str, representation: str=None):
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
    ('label', 'label declaration'),
    ('print', 'output operator'),
    ('_IDENT', 'ident'),
    ('_CONST', 'const'),
    ('_LABEL', 'label'),
]

tokens_id_map = {}
tokens_map = {}
for index, args in enumerate(tokens):
    token = Token(index, *args)
    tokens_id_map[index] = token
    tokens_map[args[0]] = token


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
| label   |   19 | label declaration          |
+---------+------+----------------------------+
| print   |   20 | output operator            |
+---------+------+----------------------------+
| _IDENT  |   21 | ident                      |
+---------+------+----------------------------+
| _CONST  |   22 | const                      |
+---------+------+----------------------------+
| _LABEL  |   23 | label                      |
+---------+------+----------------------------+
"""
