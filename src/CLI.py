import ply.lex as lex
import ply.yacc as yacc
from src.Functions import Functions
from src.Exec import Exec
# reserve words
reserve ={
    'exec': 	'EXEC',
    'mkdisk':   'MKDISK',
    'fdisk':    'FDISK',
    'size':     'SIZE',
    'fit':      'FIT',
    'unit':     'UNIT',
    'path':     'PATH', 
}

tokens = [
    'ID',
    'STRING',
    'NUMBER',
    'FILENAME',
    'PATH_DIRECTORY',
    'EQUALTO', # =
    'DASH',  # -
]+list(reserve.values())

t_EQUALTO =         r'='
t_DASH =            r'-'

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

def t_PATH_DIRECTORY(t):
    r'\/[a-zA-Z0-9_\/]*\/'
    return t

def t_FILENAME(t):
    r'[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+' 
    return t

# def t_STRING(t):
#     r'"[^"]*"'
#     t.value = t.value[1:-1]
#     return t


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
    print('Error Lexico: '+t.value[0]+' line: '+str(t.lineno)+' column: '+str(find_column(input, t)))
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos)+1
    return (token.lexpos - line_start) + 1

#sintax grammar-----------------------------------------------------------------------
def p_init(t):
    '''init :   instructions'''
    t[0] = t[1]

def p_instructions(t):
    '''
    instructions : instructions instruction
    '''
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_instructions_instruction(t):
    '''instructions :   instruction'''
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]

def p_instruction(t):
    '''
    instruction :   exec_instruction
                |   mkdisk_instruction
                |   fdisk_instruction
    
    '''
    t[0] = t[1]

def p_instruction_error_0(t):
    '''
        instruction :   error
    '''
    # error.append(Exception("Sintáctico","Error Sintáctico " + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    print("Error Sintáctico " + str(t[1].value) + " line: " + str(t.lineno(1)) + " column: " + str(find_column(input, t.slice[1])))
    t[0] = ""



def p_exec_instruction(t):
    '''exec_instruction :   EXEC PATH EQUALTO PATH_DIRECTORY FILENAME'''
    t[0] = Exec().read_file(t[4]+t[5])
    # print(t[4]+" "+t[5])


def p_mkdisk_instruction(t):
    '''mkdisk_instruction : MKDISK ID'''
    print(t[2])
    t[0] = t[1]

def p_fdisk_instruction(t):
    '''fdisk_instruction :  FDISK ID'''
    print(t[2])
    t[0] = t[1]

# def p_error(t):
#     if t:
#         print(Functions().RED+"Error "+Functions().RESET+"sintactico de tipo {} en el valor {}".format(
#             str(t.type), str(t.value)))
#     else:
#         print(Functions().RED+"Error"+Functions().RESET +" sintactico {}".format(t))


input = ''
def cli_command(command):
    # construct to lexer analyzer
    input = command
    lexer = lex.lex()
    parser = yacc.yacc()
    output = parser.parse(command)
    if output == None:
        return ""
    else: return output[0]