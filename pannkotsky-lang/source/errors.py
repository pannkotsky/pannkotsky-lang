class PKLanguageError(Exception):
    def __init__(self, message: str, line_no: int, char_no: int=None):
        char_text = f', char {char_no}' if char_no else ''
        message = f'{self.__class__.__name__} at line {line_no}{char_text}: {message}'
        self.args = (message,)


class PKLLexicalError(PKLanguageError):
    pass


class PKLSemanticError(PKLanguageError):
    pass


class PKLSyntaxError(PKLanguageError):
    pass
