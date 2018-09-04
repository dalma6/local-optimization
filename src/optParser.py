import libraries.yacc as yacc
import optLexer as lexer
#from ArithmeticError import ZeroDivisionError


tokens = lexer.tokens

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
    ('right', 'UMINUS'),
) 

names = {}

def p_program(p):
    'program : statement'
    p[0] = p[1]

def p_statement_if_gotonum(p):
    '''statement : IF condition GOTO NUMBER'''
    p[0] = ('IF' , p[2], p[4])

def p_statement_if_gotoid(p):
    '''statement : IF condition GOTO ID'''
    try:
        p[0] = ('IF' , p[2], names[p[4]])
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0]= 0

def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    names[p[1]] = p[3]
    p[0] = ('assign', p[1], ':=' , p[3])

def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]

def p_condition_id(p):
    '''condition : ID LGT NUMBER
                | ID LGT ID 
                | NUMBER LGT ID
                | NUMBER LGT NUMBER'''

    try:
        if type(p[1]) is int:
            first = ('const', p[1])
        else:
            first = ('id', p[1])
        if type(p[3]) is int:
            third = ('const', p[3])
        else:
            #third = names[p[3]]
            third = ('id', p[3])

        p[0] = (p[2], first, third)
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0]= 0
   
def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '^' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = ('+', p[1] , p[3])
    elif p[2] == '-':
        p[0] = ('-', p[1] ,p[3])
    elif p[2] == '*':
         p[0] = ('*', p[1] ,p[3])
    elif p[2] == '^':
         p[0] = ('^', p[1] ,p[3])
    elif p[2] == '/':
        try:
            a = p[1] / p[3]
            p[0] = ('/', p[1] ,p[3])
        except ZeroDivisionError:
            print("Division by 0")
            
def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = ("const", p[1])

def p_expression_name(p):
    "expression : ID"
    p[0] = ("id", p[1])

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

yacc.yacc()
