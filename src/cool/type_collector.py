from .errors import SemanticError
from .cmp import visitor, Context, SemanticErrorException
from .parser import ProgramNode, ClassDeclarationNode

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = Context()
        self.errors = errors

        # Creating built-in types
        self.context.create_type('Object')
        self.context.create_type('IO')
        self.context.create_type('Int')
        self.context.create_type('String')
        self.context.create_type('Bool')
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):       
        for def_class in node.declarations:
            self.visit(def_class)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id.lex)
        except SemanticErrorException as ex:
            self.errors.append(SemanticError((node.line, node.column), ex.text))
