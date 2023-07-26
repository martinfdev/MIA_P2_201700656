import ply.lex as lex
import ply.yacc as yacc

# reserve words
reserve ={
    'exec': 	'EXEC',
    'mkdir':    'MKDIR'
}

tokens = [
    'ID',
    'STRING',
    'NUMBER',
    'EQUALTO' # =
    'DASH'  # -
    'DOT'   # .
]+list(reserve.values())

t_EQUALTO =         r'='
t_DASH =            r'-'
t_DOT =             r'\.'

def t_DECIMALNUM(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        # print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_INTNUM(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        # print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserve.get(t.value.lower(), 'ID')    # Check for reserved words
    return t


# ignore character
t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    # error.append(Exception('Lexico', 'Error Lexico: ' +
    #              t.value[0], t.lineno, find_column(input, t)))
    print("Error Lexico {t.value[0]} {t.lineno} ")
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos)+1
    return (token.lexpos - line_start) + 1

# construct to lexer analyzer
lexer = lex.lex()