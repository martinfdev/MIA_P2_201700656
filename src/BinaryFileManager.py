import os
class BinaryFileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.status = False

        if(not self.check_status_file()):
            self.file = open(file_path, 'w')
            self.file.close()

    # if file exist or not
    def check_status_file(self):
        try:
            open(self.file_path, 'r')
            self.status_file = True
        except IOError:
            print(f'{self.file_path} ha sido creado!')
            self.status_file = False
        return self.status_file

    # fill binary file wiht data '\0' buffer
    def fill_binary_file(self, size_buffer, init_position):
        with open(self.file_path, 'ab') as file:
            file.seek(init_position)    
            file.write(b'\0' * size_buffer)
            file.flush()
            os.fsync(file.fileno())
            file.close()

    def write_binary_data(self, data, position):
        with open(self.file_path, 'r+b') as file:
            file.seek(position)
            file.write(data)
            file.close()

    def read_binary_data(self, position, size_buffer):
        with open(self.file_path, 'rb') as file:
            file.seek(position)
            data = file.read(size_buffer)
            file.close()
            return data
