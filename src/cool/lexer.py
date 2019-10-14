import ply.lex as lex


###### TOKEN LISTS ######
literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',']

reserved = {
	'CLASS',
	'INHERITS',
	'IF',
	'THEN',
	'ELSE',
	'FI',
	'WHILE',
	'LOOP',
	'POOL',
	'LET',
	'IN',
	'CASE',
	'OF',
	'ESAC',
	'NEW',
	'ISVOID',
}

ignored = [' ', '\n', '\f', '\r', '\t', '\v']

tokens = [
	# Identifiers
	'TYPE', 'ID',
	# Primitive data types
	'INTEGER', 'STRING', 'BOOL',
	# Special keywords
	'ACTION',
	# Operators
	'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT', 'NOT',
] + list(reserved)


###### TOKEN RULES ######

# Primitive data types
def t_INTEGER(t):
	r'[0-9]+'
	t.value = int(t.value)
	return t

def t_STRING(t):
	r'"[^\0\n"]*(\\\n[^\0\n"]*)*"'
	t.value = t.value[1:-1]
	return t

def t_BOOL(t):
	r't[rR][uU][eE]|f[aA][lL][sS][eE]'
	t.value = True if t.value.lower() == 'true' else False
	return t

def t_COMMENT(t):
    # r'--[^\n]+\n|\(\*[^(\*\))]+\*\)'
    r'(\(\*(.|\s)*?\*\))|(--.*)'
    pass  # Discard comments


# Other tokens with precedence before TYPE and ID
def t_NOT(t):
	r'[nN][oO][tT]'
	return t


# Identifiers
def check_RESERVED(t):
    tupper = t.value.upper()

    if tupper in reserved:
        t.type = tupper

def t_TYPE(t):
    r'[A-Z][A-Za-z0-9_]*'
    check_RESERVED(t)
    return t

def t_ID(t):
    r'[a-z][A-Za-z0-9_]*'
    check_RESERVED(t)
    return t


# Operators
t_ASSIGN = r'<-'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_EQUAL = r'='
t_INT_COMPLEMENT = r'~'


# Special keywords
t_ACTION = r'=>'


###### SPECIAL RULES ######
errors = []

def t_error(t):
    t.value = t.value[:10] + ' ...'
    errors.append(t)
    t.lexer.skip(1)

t_ignore = ''.join(ignored)

###### CREATE LEXER ######
lex.lex()

###### TOKENIZER ######
def tokenizer(code):
    line = 0
    endls = [-1] + [i for i, c in enumerate(code) if c == '\n']
    lendls = len(endls)

    tokens = []

    lex.input(code)
    while True:
        token = lex.token()

        if token is None:
            break
        
        tokens.append(token)

    # setting correct line and columns of tokens
    line = 0
    for token in tokens:
        while line < lendls and token.lexpos > endls[line]: line += 1
        token.lineno = line
        token.lexpos -= endls[line - 1]

    # setting correct line and columns of error tokens
    line = 0
    for token in errors:
        while line < lendls and token.lexpos > endls[line]: line += 1
        token.lineno = line
        token.lexpos -= endls[line - 1] 
    
    return errors, tokens