import random
import math
import datetime
import struct
import os
class Functions:
    def __init__(self):
        self.RESET = '\033[0m'
        self.RED = '\033[91m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.MAGENTA = '\033[95m'
        self.CYAN = '\033[96m'
        self.WHITE = '\033[97m'

    def get_random_mumber(self, init, end):
        return math.floor(random.uniform(init, end))

    #return time_stamp in value int
    def get_time_stamp_now(self):
        return datetime.datetime.now()
        
    #return int param is a time_stamp
    def get_time_stamp(self, time_s): # time_s is a datetime
        return  int(time_s.timestamp())

    #return time_stamp in fomrat datetime
    def get_time_stamp_obj(self, time_s): # time_s is a int
        return datetime.datetime.fromtimestamp(time_s)

    #return string to bytes
    def string_to_bytes(self, string):
        return string.encode()

    #return bytes to string
    def bytes_to_string(self, bytes):
        return bytes.decode().rstrip('\x00')

    def err_msg(self, command, message):
        print(f"{self.RED}ERROR {command}: {self.YELLOW}{message} {self.RESET}")

    def success_msg(self, command, message):
        print(f"{self.GREEN}SUCCESS {command}: {self.BLUE}{message} {self.RESET}")

    def serialize(self,format, *args):
            return struct.pack(format, *args)

    def deserialize(self, format, data):
        try:
            return struct.unpack(format, data)
        except struct.error:
            print(f"{self.RED}Error  {self.RESET}al deserializar", struct.error)
            return None

    def check_status_file(self, file_path):
        if not os.path.exists(file_path):
            return False
        try:
            open(file_path, 'rb')
            return True
        except IOError:
            print(f'{self.RED}Error {self.YELLOW} archivo {self.BLUE}{file_path}{self.YELLOW} no existe!{self.RESET}')
            return False
    
    def check_status_folder(self, folder_path):
        if not os.path.exists(folder_path):
            return False
        return True

    def get_file_name(self, file_path):
        return os.path.basename(file_path)    

    def create_folder(self, folder_path, command = ""):
        try:
            os.makedirs(folder_path)
            print(f'{self.GREEN}SUCCESS {command}: {self.YELLOW} al crear carpeta {self.BLUE}{folder_path}{self.RESET}')
            return True
        except OSError:
            print(OSError.args)
            print(f'{self.RED}WARNING {self.YELLOW} ya existe directorio {self.BLUE}{folder_path}{self.RESET}')
            return False

    def calculate_value_of_n(self, size_partition, super_block, inode, content):
        n = (size_partition - struct.calcsize(super_block.FORMATSUPERBLOCK)) / (4 + struct.calcsize(inode.FORMARTINODETABLE) + 3 * struct.calcsize(content.FORMARTCONTENT)*4)
        return math.floor(n)

    def calculte_n_with_journaling(self, size_partition, journaling  ,super_block, inode, content):
        n = (size_partition - struct.calcsize(super_block.FORMATSUPERBLOCK)) / (struct.calcsize(journaling.FORMATJOURNALING) +  4 + struct.calcsize(inode.FORMARTINODETABLE) + 3 * struct.calcsize(content.FORMARTCONTENT)*4)
        return math.floor(n)

    def funct_to_pause(self):
        input("Presione enter para continuar...")     