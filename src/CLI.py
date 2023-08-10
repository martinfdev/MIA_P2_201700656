import ply.lex as lex
import ply.yacc as yacc
from src.Functions import Functions
from src.Exec import Exec
from src.Primitive import *
import re
from src.Mkdisk import Mkdisk
# reserve words
reserve ={
    'exec': 	'EXEC',
    'mkdisk':   'MKDISK',
    'fdisk':    'FDISK',
    'path':     'PATH', 
    'size':     'SIZE',
    'fit':      'FIT',
    'unit':     'UNIT',
}

tokens = [
    'ID',
    'FILENAME',
    'DECIMALNUM',
    'INTNUM',
    'STRING',
    'COMMENTUNTLINE',
    'COMMENTMULTILINE',
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

def t_COMMENTUNTLINE(t):
    r'\#.*'
    return t

def t_COMMENTMULTILINE(t):
    r'\/\*(.|\n)*?\*\/'
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
    r'[a-zA-Z0-9_]+\.(adsj|dsk)' 
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
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
    print(f'{Functions().RED}Error Lexico: {Functions().RESET}'+t.value[0]+' line: '+str(t.lineno)+' column: '+str(find_column(input, t)))
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos)+1
    return (token.lexpos - line_start) + 1

#-----------------------------------------------------------------------sintax grammar-----------------------------------------------------------------------
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
                |   print_comments
    '''
    t[0] = t[1]

def p_instruction_error_0(t):
    '''
        instruction :   error
    '''
    print(f"{Functions().RED}Error Sintáctico {Functions().RESET}" + str(t[1].value) + " line: " + str(t.lineno(1)) + " column: " + str(find_column(input, t.slice[1])))
    t[0] = ""

def p_exec_instruction(t):
    '''exec_instruction :   EXEC DASH path_eq_pathdir'''
    t[0] = Exec(t[3]).read_file()
    # print(t[4]+" "+t[5])

def p_mkdisk_instruction(t):
    '''mkdisk_instruction  : MKDISK ls_params_mkdisk'''
    Mkdisk(t[2]).create_disk()
    t[0] = ""

def p_ls_params_mkdisk(t):
    '''ls_params_mkdisk     :   ls_params_mkdisk param_mkdisk
                            |   param_mkdisk'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_param_mkdisk(t):
    '''param_mkdisk :   DASH size_eq_intnum
                    |   DASH path_eq_pathdir
                    |   DASH fit_eq_id
                    |   DASH unit_eq_unit'''
    t[0] = t[2]

def p_fdisk_instruction(t):
    '''fdisk_instruction :  FDISK ID'''
    print(t[2])
    t[0] = t[1]

def p_path_eq_pathdir(t):
    '''path_eq_pathdir  : PATH EQUALTO PATH_DIRECTORY FILENAME
                        | PATH EQUALTO STRING'''
    if len(t) == 5:
        t[0] = Path(t[3], t[4])
    else:
        directory_regex = r'\/[a-zA-Z0-9_ !\/]*\/'
        file_name_regex = r"/([^/]+)$"
        file_name = re.search(file_name_regex, t[3])
        directory = re.search(directory_regex, t[3])
        if file_name == None:
            raise Exception("Error Sintáctico: Path inválido")
        elif directory == None:
            raise Exception("Error Sintáctico: Path inválido")
        t[0] = Path(directory.group(0), file_name.group(1))    

def p_size_eq_intnum(t):
    '''size_eq_intnum : SIZE EQUALTO INTNUM'''
    t[0] = Size(t[3])

def p_fit_eq_id(t):
    '''fit_eq_id : FIT EQUALTO ID'''
    t[0] = Fit(t[3])

def p_unit_eq_id(t):
    '''unit_eq_unit : UNIT EQUALTO ID'''
    t[0] = Unit(t[3])

def p_print_comments(t):
    '''print_comments : COMMENTUNTLINE
                      | COMMENTMULTILINE'''
    print(f'{Functions().MAGENTA}{t[1]}{Functions().RESET}')
    t[0] = ""
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
    elif  output == []:
        return ""
    else: return output[0]