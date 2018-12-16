import helpers

"""
0: initial state
-1: char return
1: ident in progress
2: number in progress
3: assignment in progress
4-11: simple states
12: < or <=
13: > or >=
14: == in progress
15: space in progress
16: ident completed
17: number completed
18: assignment completed
19: space completed
"""


class LexicalError(Exception):
    pass


class State:
    index = None
    is_initial = False
    is_final = False
    with_return = False
    label = None
    transitions_map = {}

    @classmethod
    def _get_next_state(cls, c):
        raise NotImplementedError

    @classmethod
    def get_next_state(cls, c):
        if not helpers.is_symbol(c):
            raise LexicalError(f'Unexpected token: {c}')
        if c in cls.transitions_map:
            return cls.transitions_map[c]
        state = cls._get_next_state(c)
        if state is None:
            raise LexicalError(f'Unexpected token: {c}')
        return state


class FinalState(State):
    is_final = True

    @classmethod
    def _get_next_state(cls, c):
        return 0


class FinalStateWithReturn(State):
    is_final = True
    with_return = True

    @classmethod
    def _get_next_state(cls, c):
        return 0


class State0(State):
    index = 0
    is_initial = True
    label = "Initial state"

    transitions_map = {
        ':': 3,
        '+': 4,
        '-': 5,
        '*': 6,
        '/': 7,
        '^': 8,
        '(': 9,
        ')': 10,
        '\n': 11,
        '<': 12,
        '>': 13,
        '=': 14,
        ' ': 15,
    }

    @classmethod
    def _get_next_state(cls, c):
        if helpers.is_letter(c):
            return 1
        if helpers.is_digit(c):
            return 2


class State1(State):
    index = 1
    label = "Ident in progress"

    @classmethod
    def _get_next_state(cls, c):
        if helpers.is_digit(c) or helpers.is_letter(c):
            return 1
        return 16


class State2(State):
    index = 2
    label = "Number in progress"

    @classmethod
    def _get_next_state(cls, c):
        if helpers.is_digit(c):
            return 2
        if helpers.is_letter(c):
            raise LexicalError(f'Unexpected token: {c}')
        return 17


class State3(State):
    index = 3
    label = "Assignment in progress"

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 18


class State4(FinalState):
    index = 4


class State5(FinalState):
    index = 5


class State6(FinalState):
    index = 6


class State7(FinalState):
    index = 7


class State8(FinalState):
    index = 8


class State9(FinalState):
    index = 9


class State10(FinalState):
    index = 10


class State11(FinalState):
    index = 11


class State12(State):
    index = 12
    label = "Less or LTE"

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 21
        return 22


class State13(State):
    index = 13
    label = "Greater or GTE"

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 23
        return 24


class State14(State):
    index = 14
    label = "Equality in progress 1"

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 20


class State15(State):
    index = 15
    label = "Space in progress"

    @classmethod
    def _get_next_state(cls, c):
        if c == ' ':
            return 15
        return 19


class State16(FinalStateWithReturn):
    index = 16
    label = "Ident completed"


class State17(FinalStateWithReturn):
    index = 17
    label = "Number completed"


class State18(FinalState):
    index = 18
    label = "Assignment completed"


class State19(FinalStateWithReturn):
    index = 19
    label = "Space completed"


class State20(FinalState):
    index = 20
    label = "Equality completed"


class State21(FinalState):
    index = 21
    label = "LTE completed"


class State22(FinalStateWithReturn):
    index = 22
    label = "Less completed"


class State23(FinalState):
    index = 23
    label = "GTE completed"


class State24(FinalStateWithReturn):
    index = 24
    label = "Greater completed"


states_map = {
    0: State0,
    1: State1,
    2: State2,
    3: State3,
    4: State4,
    5: State5,
    6: State6,
    7: State7,
    8: State8,
    9: State9,
    10: State10,
    11: State11,
    12: State12,
    13: State13,
    14: State14,
    15: State15,
    16: State16,
    17: State17,
    18: State18,
    19: State19,
    20: State20,
    21: State21,
    22: State22,
    23: State23,
    24: State24,
}

final_state_token_type_map = {
    16: 'Ident',
    17: 'Const',
}
