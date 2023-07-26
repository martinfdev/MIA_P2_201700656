class BinaryFileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.exist_file =  False

    # if file exist or not
    def exist_file(self):
        try:
            open(self.file_path, 'x')
            self.exist_file = True
        except IOError:
            self.exist_file = False
        return self.exist_file

    # fill binary file wiht data '\0'
    def fill_binary_file(self, size_buffer):
        if(self.exist_file(self.file_path)):
            with open(self.file_path, 'ab') as file:    
                pass

    def write_binary_data(self, data):
        with open(self.file_path, 'wb') as file:
            file.write(data)
            

    def read_binary_data(self):
        with open(self.file_path, 'rb') as file:
            return file.read()
