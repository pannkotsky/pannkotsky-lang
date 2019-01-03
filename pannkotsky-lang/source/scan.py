from .errors import PKLLexicalError, PKLSemanticError
from .states import final_state_token_type_map, states_map, UnexpectedTokenError
from .tokens import tokens_map, tokens_id_map, Token


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


class Scanner:
    def __init__(self, input_f):
        self.scan_tokens = []
        self.idents_map = {}
        self.constants_map = {}
        self.labels_map = {}
        self.output = []

        self.numline = 1
        self.numchar = 1
        self.current_state = states_map.get(0)
        self.current_char = ''
        self.current_token = ''

        self.input_file = input_f

    def scan(self):
        for line in self.input_file:
            self.process_line(line)

    def get_next_state(self):
        try:
            state_index = self.current_state.get_next_state(self.current_char)
            return states_map.get(state_index)
        except UnexpectedTokenError:
            raise PKLLexicalError(f'Unexpected token: {self.current_char}',
                                  self.numline, self.numchar)

    def process_line(self, line):
        self.numchar = 0
        while self.numchar < len(line):
            self.numchar += 1
            self.current_char = line[self.numchar - 1]
            self.current_state = self.get_next_state()
            if not self.current_state.with_return and not self.current_state.is_initial:
                self.current_token += self.current_char
            else:
                self.numchar -= 1
            self.write_output()
            if self.current_state.is_final:
                self.save_token()
                self.current_token = ''
        self.numline += 1

    def save_token(self):
        if not self.current_token.strip(' '):
            return
        token_repr = self.current_token
        token_id = None
        ident_const_id = ''
        if self.current_token in tokens_map:
            token_obj = tokens_map[self.current_token]
            token_id = token_obj.id
            token_repr = token_obj.representation
        else:
            token_type = final_state_token_type_map.get(self.current_state.index)
            if token_type == 'Ident':
                is_var_declared = self.scan_tokens and self.scan_tokens[-1].token_repr == 'var'
                is_label_declared = self.scan_tokens and self.scan_tokens[-1].token_repr == 'label'
                if self.current_token in self.idents_map:
                    if is_var_declared or is_label_declared:
                        raise PKLSemanticError(f'Repeated identifier declaration: {self.current_token}',
                                               self.numline, self.numchar)
                    token_id = tokens_map['_IDENT'].id
                    ident_const_id = self.idents_map[self.current_token]
                elif self.current_token in self.labels_map:
                    if is_var_declared or is_label_declared:
                        raise PKLSemanticError(f'Repeated identifier declaration: {self.current_token}',
                                               self.numline, self.numchar)
                    token_id = tokens_map['_LABEL'].id
                    ident_const_id = self.labels_map[self.current_token]
                elif is_var_declared:
                    token_id = tokens_map['_IDENT'].id
                    ident_const_id = self.idents_map.setdefault(
                        self.current_token, len(self.idents_map))
                elif is_label_declared:
                    token_id = tokens_map['_LABEL'].id
                    ident_const_id = self.labels_map.setdefault(
                        self.current_token, len(self.labels_map))
                else:
                    raise PKLSemanticError(f'Undeclared identifier: {self.current_token}',
                                           self.numline, self.numchar)
            elif token_type == 'Const':
                token_id = tokens_map['_CONST'].id
                ident_const_id = self.constants_map.setdefault(
                    self.current_token, len(self.constants_map))
        self.scan_tokens.append(ScanToken(
            self.numline,
            token_repr,
            token_id,
            ident_const_id
        ))

    def write_output(self):
        self.output.append([
            self.numline,
            self.numchar,
            self.current_char,
            self.current_state.index,
            self.current_token,
        ])
