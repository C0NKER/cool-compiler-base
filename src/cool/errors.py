class COOLError:
    def __init__(self, name, pos, body):
        self.name = name
        self.pos = pos
        self.body = body

    def __str__(self):
        return f'{self.pos} - {self.name}: {self.body}'

    __repr__ = __str__

class CompilerError(COOLError):
    def __init__(self, pos, body):
        super().__init__('CompilerError', pos, body)

class LexicographicError(COOLError):
    def __init__(self, pos, body):
        super().__init__('LexicographicError', pos, body)

class SyntacticError(COOLError):
    def __init__(self, pos, body):
        super().__init__('SyntacticError', pos, body)

class NamexError(COOLError):
    def __init__(self, pos, body):
        super().__init__('NameError', pos, body)

class TypexError(COOLError):
    def __init__(self, pos, body):
        super().__init__('TypeError', pos, body)

class AttributexError(COOLError):
    def __init__(self, pos, body):
        super().__init__('AttributeError', pos, body)

class SemanticError(COOLError):
    def __init__(self, pos, body):
        super().__init__('SemanticError', pos, body)