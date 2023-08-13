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
    def get_time_stamp(self):
        time_s = datetime.datetime.now()
        return  int(time_s.timestamp())
    
    #return time_stamp in fomrat datetime
    def get_time_stamp_obj(self, time_s):
        return datetime.datetime.fromtimestamp(time_s)

    #return string to bytes
    def string_to_bytes(self, string):
        return string.encode('utf-8')

    #return bytes to string
    def bytes_to_string(self, bytes):
        return bytes.decode('utf-8')

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
            open(file_path, 'r')
            return True
        except IOError:
            print(f'{file_path} ha sido creado!')
            return False
        
    def get_file_name(self, file_path):
        return os.path.basename(file_path)    
      