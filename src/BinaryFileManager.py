import os
class BinaryFileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.status_file =  False

    # if file exist or not
    def check_status_file(self):
        try:
            open(self.file_path, 'r')
            self.status_file = True
        except IOError:
            print(f'{self.file_path} does not exist')
            self.status_file = False
        return self.status_file

    # fill binary file wiht data '\0' buffer
    def fill_binary_file(self, size_buffer):
        if(not self.check_status_file()):
            with open(self.file_path, 'ab') as file:    
               file.write(b'\0' * size_buffer)
        else:
            print(f'{self.file_path} already exist')


    def write_binary_data(self, data, position):
        with open(self.file_path, 'w+b') as file:
            file.write(data)
            

    def read_binary_data(self, buffet, postion):
        with open(self.file_path, 'rb') as file:
            return file.read()
