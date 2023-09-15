from src.Primitive import Path
from src.Functions import Functions as fn
class Mkdir:
    def __init__(self, list_params) -> None:
        self.list_params = list_params
        self.path = ""
        self.r = False

    def execute(self, list_mounts):
        for param in self.list_params:
            if isinstance(param, Path):
                self.path = param.get_value()
            elif param == "r":
                self.r = True

        if self.path == "":
            fn().err_msg("MKDIR", "No se ha especificado la ruta.")
            return
        if list_mounts == []:
            fn().err_msg("MKDIR", "No hay particiones montadas.")
            return

