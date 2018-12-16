import helpers


class LexicalError(Exception):
    pass


class State:
    index = None
    is_initial = False
    is_final = False
    with_return = False
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
    """ Initial state """
    index = 0
    is_initial = True

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
    """ Ident in progress """
    index = 1

    @classmethod
    def _get_next_state(cls, c):
        if helpers.is_digit(c) or helpers.is_letter(c):
            return 1
        return 16


class State2(State):
    """ Const in progress """
    index = 2

    @classmethod
    def _get_next_state(cls, c):
        if helpers.is_digit(c):
            return 2
        if helpers.is_letter(c):
            raise LexicalError(f'Unexpected token: {c}')
        return 17


class State3(State):
    """ Assignment in progress """
    index = 3

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 18


class State4(FinalState):
    """ + """
    index = 4


class State5(FinalState):
    """ - """
    index = 5


class State6(FinalState):
    """ * """
    index = 6


class State7(FinalState):
    """ / """
    index = 7


class State8(FinalState):
    """ ^ """
    index = 8


class State9(FinalState):
    """ ( """
    index = 9


class State10(FinalState):
    """ ) """
    index = 10


class State11(FinalState):
    """ \n """
    index = 11


class State12(State):
    """ Less or LTE """
    index = 12

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 21
        return 22


class State13(State):
    """ Greater or GTE """
    index = 13

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 23
        return 24


class State14(State):
    """ Equality in progress 1 """
    index = 14

    @classmethod
    def _get_next_state(cls, c):
        if c == '=':
            return 20


class State15(State):
    """ Space in progress """
    index = 15

    @classmethod
    def _get_next_state(cls, c):
        if c == ' ':
            return 15
        return 19


class State16(FinalStateWithReturn):
    """ Ident completed """
    index = 16


class State17(FinalStateWithReturn):
    """ Number completed """
    index = 17


class State18(FinalState):
    """ Assignment completed """
    index = 18


class State19(FinalStateWithReturn):
    """ Space completed """
    index = 19


class State20(FinalState):
    """ Equality completed """
    index = 20


class State21(FinalState):
    """ LTE completed """
    index = 21


class State22(FinalStateWithReturn):
    """ Less completed """
    index = 22


class State23(FinalState):
    """ GTE completed """
    index = 23


class State24(FinalStateWithReturn):
    """ Greater completed """
    index = 24


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
