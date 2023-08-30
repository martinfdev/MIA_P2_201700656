import re
import ply.lex as lex
import ply.yacc as yacc
from src.Functions import Functions
from src.Exec import Exec
from src.Primitive import *
from src.Mkdisk import Mkdisk
from src.Rmdisk import Rmdisk
from src.Fdisk import Fdisk
from src.Mount import Mount
from src.Unmount import Unmount
from src.Mkfs import Mkfs
from src.Rep import REP
# reserve words
reserve ={
    'execute': 	'EXECUTE',
    'mkdisk':   'MKDISK',
    'rmdisk':   'RMDISK',
    'fdisk':    'FDISK',
    'rep':      'REP',
    'path':     'PATH', 
    'size':     'SIZE',
    'fit':      'FIT',
    'unit':     'UNIT',
    'name':     'NAME',
    'type':     'TYPE',
    'add':      'ADD',
    'delete':   'DELETE',
    'mount':    'MOUNT',
    'unmount':  'UNMOUNT',
    'id':       'ID',
    'mkfs':     'MKFS',
    'fs':       'FS',
    'pause':    'PAUSE'
}

tokens = [
    'IDENTIFIER',
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

def t_IDENTIFIER(t):
    r'[a-zA-Z_0-9][a-zA-Z_0-9]*'
    t.type = reserve.get(t.value.lower(), 'IDENTIFIER')    # Check for reserved words
    return t

def t_INTNUM(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        # print("Integer value too large %d", t.value)
        t.value = 0
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
    instruction :   execute_instruction
                |   mkdisk_instruction
                |   rmdisk_instruction
                |   fdisk_instruction
                |   print_comments
                |   mount_instruction
                |   unmount_instruction
                |   mkfs_instruction
                |   rep_instruction
    '''
    t[0] = t[1]

def p_instruction_error_0(t):
    '''
        instruction :   error
    '''
    print(f"{Functions().RED}Error Sintáctico {Functions().RESET}" + str(t[1].value) + " line: " + str(t.lineno(1)) + " column: " + str(find_column(input, t.slice[1])))
    t[0] = ""

def p_instruction_pause(t):
    '''instruction : PAUSE'''
    Functions().funct_to_pause()
    t[0] = ""

def p_execute_instruction(t):
    '''execute_instruction :   EXECUTE DASH path_eq_pathdir'''
    t[0] = Exec(t[3]).read_file()
    # print(t[4]+" "+t[5])

def p_mkdisk_instruction(t):
    '''mkdisk_instruction  : MKDISK ls_params_mkdisk'''
    Mkdisk(t[2]).execute_mkdisk()
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

def p_rmdisk_instruction(t):
    '''rmdisk_instruction : RMDISK DASH path_eq_pathdir'''
    Rmdisk(t[3]).execute_rmdisk()
    t[0] = ""

def p_fdisk_instruction(t):
    '''fdisk_instruction  : FDISK ls_params_fdisk'''
    Fdisk(t[2]).executefdisk()
    t[0] = ""

def p_ls_params_fdisk(t):
    '''ls_params_fdisk      :   ls_params_fdisk param_fdisk
                            |   param_fdisk'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_param_fdisk(t):
    '''param_fdisk  :   DASH size_eq_intnum
                    |   DASH path_eq_pathdir
                    |   DASH name_eq_id
                    |   DASH unit_eq_unit
                    |   DASH type_eq_id
                    |   DASH fit_eq_id
                    |   DASH delete_eq_id
                    |   DASH add_eq_intnum'''
    t[0] = t[2]

def p_mount_instruction(t):
    '''mount_instruction    :   MOUNT ls_params_mount'''
    mount = Mount(t[2]).execute_mount()
    if mount != None:
        list_mount_partition.append(mount)
    t[0] = ''

def p_ls_params_mount(t):
    '''ls_params_mount      :   ls_params_mount param_mount
                            |   param_mount'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_param_mount(t):
    '''param_mount  :   DASH path_eq_pathdir
                    |   DASH name_eq_id'''
    t[0] = t[2]    

def p_unmount_instruction(t):
    '''unmount_instruction  :   UNMOUNT DASH id_eq_id'''
    Unmount(t[3]).execute_unmount(list_mount_partition)
    t[0] = ''

def p_mkfs_instruction(t):
    '''mkfs_instruction : MKFS ls_params_mkfs'''
    Mkfs(t[2]).execute_mkfs(list_mount_partition)
    t[0] = ""

def p_ls_params_mkfs(t):
    '''ls_params_mkfs       :   ls_params_mkfs param_mkfs
                            |   param_mkfs'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_param_mkfs(t):
    '''param_mkfs   :   DASH id_eq_id
                    |   DASH type_eq_id
                    |   DASH fs_eq_id'''
    t[0] = t[2]        


def p_rep_instruction(t):
    '''rep_instruction :    REP path_eq_pathdir'''
    REP(t[2]).execute_rep()
    t[0] = ""

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
    '''fit_eq_id : FIT EQUALTO IDENTIFIER'''
    t[0] = Fit(t[3])

def p_unit_eq_id(t):
    '''unit_eq_unit : UNIT EQUALTO IDENTIFIER'''
    t[0] = Unit(t[3])

def p_name_eq_id(t):
    '''name_eq_id   :   NAME EQUALTO IDENTIFIER
                    |   NAME EQUALTO STRING'''
    t[0] = ID(t[3])

def p_type_eq_id(t):
    '''type_eq_id : TYPE EQUALTO IDENTIFIER'''
    t[0] = Type(t[3])

def p_delete_eq_id(t):
    '''delete_eq_id : DELETE EQUALTO IDENTIFIER'''
    t[0] = Delete(str(t.lineno(1)), str(find_column(input, t.slice[1])), t[3])

def p_add_eq_intnum(t):
    '''add_eq_intnum : ADD EQUALTO INTNUM'''
    t[0] = Add(str(t.lineno(1)), str(find_column(input, t.slice[1])), t[3])  
    
def p_print_comments(t):
    '''print_comments : COMMENTUNTLINE
                      | COMMENTMULTILINE'''
    print(f'{Functions().MAGENTA}{t[1]}{Functions().RESET}')
    t[0] = ""

def p_id_eq_id(t):
    '''id_eq_id : ID EQUALTO IDENTIFIER'''
    t[0] = ID(t[3])

def p_fs_eq_id(t):
    '''fs_eq_id : FS EQUALTO IDENTIFIER'''
    t[0] = FS(t[3])
# def p_error(t):
#     if t:
#         print(Functions().RED+"Error "+Functions().RESET+"sintactico de tipo {} en el valor {}".format(
#             str(t.type), str(t.value)))
#     else:
#         print(Functions().RED+"Error"+Functions().RESET +" sintactico {}".format(t))
input = ''
list_mount_partition = []
def cli_command(command):
    # construct to lexer analyzer
    global input 
    global list_mount_partition
    input = command
    list_mount_partition = []
    lexer = lex.lex()
    parser = yacc.yacc()
    output = parser.parse(command)
    if output == None:
        return ""
    elif  output == []:
        return ""
    else: return output[0]