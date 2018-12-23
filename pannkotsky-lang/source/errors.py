import sys


class LanguageError(Exception):
    def __init__(self, message, line_no, char_no):
        message = f'{self.__class__.__name__} at line {line_no}, char {char_no}: {message}'
        self.args = (message,)
        sys.exit(self)


class LexicalError(LanguageError):
    pass


class SemanticError(LanguageError):
    pass
