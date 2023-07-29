from src.Functions import *
class Exec:
    def __init__(self) -> None:
        pass

    def read_file(self, path):
        try:
            with open(path, "r") as file:
                content_txt_file =  file.read()
                file.close()
                return content_txt_file
        except IOError as e:
            Functions().err_msg("EXEC", "no se puede leer el archivo "+str(e.filename))
            return ""