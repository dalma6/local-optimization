import libraries.lex as lex


reserved = (
    'IF',
    'GOTO',
    'IFFALSE',
    'RETURN'
)

tokens = reserved + (
   'NUMBER',
   'ID',
   'ASSIGN',
   'LGT'
) 

literals = ['=', '+', '-', '*', '/', '(', ')']

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

def t_LGT(t):
    r'(<=)|(>=)|[<>]'
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Leksicka greska bi trebalo da prekine program, zar ne?
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    #t.lexer.skip(1)
	exit()

lexer = lex.lex(debug=0)

test_data = '''
a_1 := x + y 
IFFALSE x GOTO 4
b := 3 - y 
c := 2 * y 
IF c > 0 GOTO 9
d := a + c'''

'''
lexer.input(test_data)

Gde cemo ovde proveriti da li je ulaz ispravan i zvati gresku?
while True:
    tok = lexer.token()
    if not tok: 
        break     
    print(tok)

'''