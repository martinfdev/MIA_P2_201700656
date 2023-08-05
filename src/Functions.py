import random
import math
import datetime
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

    def random_mumber(self, init, end):
        return math.floor(random.uniform(init, end))

    def time_stamp_obj(self):
        time_s = datetime.datetime.now()
        print(time_s.day)
        return time_s

    def err_msg(self, command, message):
        print(f"{self.RED}ERROR {command}: {self.YELLOW}{message} {self.RESET}")
        # print(f"{self.RED}USAGE: {command}")
        # print(f"{self.RED}EXAMPLE: {command} 100")

    def success_msg(self, command, message):
        print(f"{self.GREEN}SUCCESS {command}: {self.BLUE}{message} {self.RESET}")    