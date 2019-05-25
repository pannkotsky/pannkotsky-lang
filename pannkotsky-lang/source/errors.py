class PKLanguageError(Exception):
    def __init__(self, message: str, line_no: int=None, char_no: int=None):
        line_text = f' at line {line_no}' if line_no else ''
        char_text = f', char {char_no}' if char_no else ''
        message = f'{self.__class__.__name__}{line_text}{char_text}: {message}'
        self.args = (message,)


class PKLLexicalError(PKLanguageError):
    pass


class PKLSemanticError(PKLanguageError):
    pass


class PKLSyntaxError(PKLanguageError):
    pass
