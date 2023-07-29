import random
import math
import datetime
class Functions:
    def __init__(self):
        pass

    def random_mumber(self, init, end):
        return math.floor(random.uniform(init, end))

    def time_stamp_obj(self):
        time_s = datetime.datetime.now()
        print(time_s.day)
        return time_s    