from src.Functions import *
from src.Primitive import *
class Exec:
    def __init__(self, path_file=None):
        self.path_file = path_file

    def read_file(self):
        if self.path_file == None:
            Functions().err_msg("EXEC", "no se ha especificado el archivo")
            return ""
        path = self.path_file.get_value()
        try:
            with open(path, "r") as file:
                content_txt_file =  file.read()
                file.close()
                Functions().success_msg("EXEC", "archivo leido correctamente "+self.path_file.filename)
                return content_txt_file
        except IOError as e:
            Functions().err_msg("EXEC", "no se puede leer el archivo "+str(e.filename))
            return ""