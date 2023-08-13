from src.Functions import Functions as fn
import os
class BinaryFileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    # create binary file
    def create_file(self):
        function = fn()
        file_name = function.get_file_name(self.file_path)
        try:
            with open(self.file_path, 'wb') as file:
                file.close()
                print(f'{function.GREEN}{file_name} {function.RESET} ha sido creado!')
                return True
        except IOError:
            print(f'{function.RED}Error Archivo {function.RESET} al crear {file_name}')
            return False

    # fill binary file wiht data '\0' buffer
    def fill_binary_file(self, size_buffer, init_position):
        function = fn()
        if not function.check_status_file(self.file_path):
            print(f"{function.RED}Error Archivo {function.RESET}al escribir en {function.YELLOW}{self.file_path}{function.RESET} no existe!")
            return
        try:
            with open(self.file_path, 'r+b') as file:
                file.seek(init_position)    
                file.write(b'\0' * size_buffer)
                file.flush()
                os.fsync(file.fileno())
        except IOError:
            print(f'{function.RED}Error Archivo {function.RESET}al escribir en {function.BLUE}{self.file_path}{function.RESET}')        

    def write_binary_data(self, data, position):
        function = fn()
        try:
            with open(self.file_path, 'r+b') as file:
                file.seek(position)
                file.write(data)
        except IOError:
            print(f'{function.RED}Error Archivo {function.RESET}al escribir en {function.BLUE}{self.file_path}{function.RESET}')

    def read_binary_data(self, position, size_buffer):
        function = fn()
        try:
            with open(self.file_path, 'rb') as file:
                file.seek(position)
                data = file.read(size_buffer)
                return data
        except IOError:
            print(f'{function.RED}Error Archivo {function.RESET} al leer en {function.BLUE}{self.file_path}{function.RESET}')
            return None    
