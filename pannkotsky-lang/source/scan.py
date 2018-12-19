#!/usr/bin/env python3
import csv

from .states import final_state_token_type_map, states_map, LexicalError
from .tokens import tokens_map


class Scanner:
    def __init__(self, input_f, output_f):
        self.scan_tokens = []
        self.idents_map = {}
        self.constants_map = {}

        self.numline = 1
        self.numchar = 1
        self.current_state = states_map.get(0)
        self.current_char = ''
        self.current_token = ''

        self.input_file = input_f

        fieldnames = ['Numline', 'Numchar', 'Char', 'State', 'Token']
        self.output_writer = csv.DictWriter(output_f, fieldnames)
        self.output_writer.writeheader()

    def scan(self):
        for line in self.input_file:
            self.process_line(line)

    def get_next_state(self):
        try:
            state_index = self.current_state.get_next_state(self.current_char)
            return states_map.get(state_index)
        except LexicalError as e:
            print(f'Lexical error at {self.numline}:{self.numchar} {e}')
            exit(-1)

    def process_line(self, line):
        self.numchar = 0
        while self.numchar < len(line):
            self.write_output()
            self.numchar += 1
            self.current_char = line[self.numchar - 1]
            self.current_state = self.get_next_state()
            if not self.current_state.with_return and not self.current_state.is_initial:
                self.current_token += self.current_char
            else:
                self.numchar -= 1
            if self.current_state.is_final:
                self.save_token()
                self.current_token = ''
        self.numline += 1

    def save_token(self):
        # TODO: detect redeclaration of variable, undeclared variable
        # TODO: detect labels
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
                token_id = tokens_map['_IDENT'].id
                ident_const_id = self.idents_map.setdefault(
                    self.current_token, len(self.idents_map) + 1)
            elif token_type == 'Const':
                token_id = tokens_map['_CONST'].id
                ident_const_id = self.constants_map.setdefault(
                    self.current_token, len(self.constants_map) + 1)
        self.scan_tokens.append([
            self.numline,
            token_repr,
            token_id,
            ident_const_id
        ])

    def write_output(self):
        self.output_writer.writerow({
            'Numline': self.numline,
            'Numchar': self.numchar,
            'Char': self.current_char,
            'State': self.current_state.index,
            'Token': self.current_token,
        })
