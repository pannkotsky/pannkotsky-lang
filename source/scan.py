#!/usr/bin/env python3

import csv
import os
import sys
import time

from states import states_map, LexicalError


class Scanner:
    def __init__(self, input_f, output_f):
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
                self.current_token = ''
        self.numline += 1

    def write_output(self):
        self.output_writer.writerow({
            'Numline': self.numline,
            'Numchar': self.numchar,
            'Char': self.current_char,
            'State': self.current_state.index,
            'Token': self.current_token,
        })


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scan.py <input_filename>")
        exit(-1)
    with open(sys.argv[1]) as input_file:
        output_fname = input_file.name.rsplit('/', 1)[-1]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, 'outputs', f'{output_fname}_{time.time()}.csv')
        with open(output_path, 'w') as output_file:
            scanner = Scanner(input_file, output_file)
            scanner.scan()
