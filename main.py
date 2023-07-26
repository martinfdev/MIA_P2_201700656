from src.BinaryFileManager import BinaryFileManager

if __name__ == "__main__":
    file_manager = BinaryFileManager("archivo.bin")
    data_binary = b'\0'
    buffer = data_binary * 1024
    status = file_manager.exist_file()
    # file_manager.write_binary_data(buffer)