class Token:
    def __init__(self, id, token, description=''):
        self.id = id
        self.token = token
        self.description = description


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
    ('\n', 'newline'),
    ('repeat', 'loop operators block start'),
    ('until', 'loop condition start'),
    ('if', 'condition start'),
    (' ', 'space'),
    ('goto', 'goto statement'),
    ('label', 'label for goto'),
    # input
    # output
]

tokens_id_map = {}
tokens_map = {}
for index, args in enumerate(tokens):
    token = Token(index, *args)
    tokens_id_map[index] = token
    tokens_map[args[0]] = token
