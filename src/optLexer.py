import libraries.lex as lex


reserved = (
    'IF',
    'GOTO',
    'IFFALSE'
)

tokens = reserved + (
    'NUMBER',
    'ID',
    'ASSIGN',
    'SHL',
    'SHR',
    'LGT'
)

literals = ['=', '+', '-', '*', '/', '(', ')', '^', '<', '>']


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ASSIGN(t):
    r':='
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = t.value
    return t


def t_SHL(t):
    r'<<'
    return t


def t_SHR(t):
    r'>>'
    return t


def t_LGT(t):
    r'(<=)|(>=)|(<>)|(==)|[>]|[<]'
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    exit()


lexer = lex.lex(debug=0)
