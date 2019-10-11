from cool import tokenizer
from cool import CoolParser, CoolGrammar
from cool.cmp import evaluate_reverse_parse, Token
from cool import FormatVisitor, TypeCollector, TypeBuilder, TypeChecker

import sys

clfile = sys.argv[1]

try:
    fd = open(clfile, 'r')
    text = fd.read()
    fd.close()
except FileNotFoundError:
    print('(0, 0) - CompilerError: El archivo', clfile, 'no se pudo encontrar.')
    exit(1)

# Lexer ...
errors, tokens = tokenizer(text)

if errors:
    print('(', errors[0].lineno, ',', errors[0].lexpos, ') - LexicographicError: no se reconoce el token', errors[0].value)
    exit(1)

tokens = [Token(t.value, CoolGrammar[t.type.lower()], t.lineno, t.lexpos) for t in tokens]
tokens.append(Token('$', CoolGrammar.EOF))

# Parser ...
parse, operations = CoolParser(tokens)

if not operations:
    print('(', parse.line, ',', parse.column, ') - SyntacticError: no se esperaba el token', parse.lex)
    exit(1)

# Semantic ...
ast = evaluate_reverse_parse(parse, operations, tokens)
formatter = FormatVisitor()
# tree = formatter.visit(ast)

errors = []

collector = TypeCollector(errors)
collector.visit(ast)
context = collector.context

builder = TypeBuilder(context, errors)
builder.visit(ast)

checker = TypeChecker(context, errors)
scope = checker.visit(ast)


if errors:
    for error in errors:
        print(error)
    exit(1)

exit(0)