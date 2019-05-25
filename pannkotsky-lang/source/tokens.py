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
    ('!=', 'not equal to'),
    ('var', 'variable declaration'),
    ('\n', 'newline', '\\n'),
    ('repeat', 'loop operators block start'),
    ('until', 'loop condition start'),
    ('if', 'condition start'),
    ('goto', 'goto statement'),
    ('label', 'label declaration'),
    ('print', 'output operator'),
    ('input', 'input operator'),
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


class ScanToken:
    def __init__(self, numline: int, token_repr: str, token_id: int, ident_id: int):
        self.numline = numline
        self.token_repr = token_repr
        self.token_id = token_id
        self.ident_id = ident_id

    def to_table_row(self):
        return (
            self.numline,
            self.token_repr,
            self.token_id,
            self.ident_id
        )

    def get_token_object(self) -> Token:
        return tokens_id_map.get(self.token_id)

    def get_token_str(self) -> str:
        return self.get_token_object().token

    def __str__(self):
        return self.token_repr
