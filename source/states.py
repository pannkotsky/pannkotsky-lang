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


class ScanError(Exception):
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
            raise ScanError(f'Unexpected token: {c}')
        if c in cls.transitions_map:
            return cls.transitions_map[c]
        state = cls._get_next_state(c)
        if state is None:
            raise ScanError(f'Unexpected token: {c}')
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


class StateMinus1(State):
    index = -1
    label = "Return char and go to initial state"

    @classmethod
    def _get_next_state(cls, c):
        return 0


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
            raise ScanError(f'Unexpected token: {c}')
        return 17


class State3(State):
    index = 3
    label = "Assignment in progress"

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 18
        raise ScanError(f'Unexpected token: {c}')


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


states_map = {
    0: State0,
    -1: StateMinus1,
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
    15: State15,
    16: State16,
    17: State17,
    18: State18,
    19: State19,
}

final_state_token_type_map = {
    4: '+',
    5: '-',
    6: '*',
    7: '/',
    8: '^',
    9: '(',
    10: ')',
    11: '\n',
    16: 'Ident',
    17: 'Number',
    18: ':=',
    19: None
}
