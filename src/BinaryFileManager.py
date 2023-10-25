from src.Functions import Functions as fn
import os
class BinaryFileManager:
    def __init__(self, file_path, arr_output_result) -> None:
        self.file_path = file_path
        self.arr_output_result = arr_output_result

    # create binary file
    def create_file(self):
        function = fn(self.arr_output_result)
        file_name = function.get_file_name(self.file_path)
        try:
            with open(self.file_path, 'wb') as file:
                file.close()
                # print(f'{function.GREEN}{file_name} {function.RESET} ha sido creado!')
                self.arr_output_result.append(f'{file_name} ha sido creado!')
                return True
        except IOError:
            # print(f'{function.RED}Error Archivo {function.RESET} al crear {file_name}')
            self.arr_output_result.append(f'Error Archivo al crear {file_name}')
            return False

    # fill binary file wiht data '\x00' buffer
    def fill_binary_file(self, size_buffer, init_position):
        function = fn(self.arr_output_result)
        if not function.check_status_file(self.file_path):
            # print(f"{function.RED}Error Archivo {function.RESET}al escribir en {function.YELLOW}{self.file_path}{function.RESET} no existe!")
            self.arr_output_result.append(f"Error Archivo al escribir en {self.file_path} no existe!")
            return False
        try:
            with open(self.file_path, 'r+b') as file:
                file.seek(init_position)
                buffer = b'\x00' * size_buffer
                file.write(buffer)
                return True 
        except IOError:
            # print(f'{function.RED}Error Archivo {function.RESET}al escribir en {function.BLUE}{self.file_path}{function.RESET}')        
            self.arr_output_result.append(f'Error Archivo al escribir en {self.file_path}')
            return False

    def write_binary_data(self, data, position):
        function = fn(self.arr_output_result)
        try:
            with open(self.file_path, 'rb+') as file:
                file.seek(position)
                file.write(data)
        except IOError:
            # print(f'{function.RED}Error Archivo {function.RESET}al escribir en {function.BLUE}{self.file_path}{function.RESET}')
            self.arr_output_result.append(f'Error Archivo al escribir en {self.file_path}')

    def read_binary_data(self, position, size_buffer):
        function = fn(self.arr_output_result)
        try:
            with open(self.file_path, 'rb') as file:
                file.seek(position)
                data = file.read(size_buffer)
                return data
        except IOError:
            # print(f'{function.RED}Error Archivo {function.RESET} al leer en {function.BLUE}{self.file_path}{function.RESET}')
            self.arr_output_result.append(f'Error Archivo al leer en {self.file_path}')
            return None    
