from src.Primitive import  *
from src.Functions import Functions
from src.BinaryFileManager import BinaryFileManager as bfm
class Mkdisk:
    def __init__(self, list_params) -> None:
        self._list_params = list_params
        self._size = -1
        self._path = ""
        self._fit = "FF"
        self._unit = "M"
        self._file_name = ""

    def create_disk(self):
        if not self._set_values():
            Functions().err_msg("MKDISK", "No se pudo crear el disco "+Functions().CYAN+self._file_name)




    def _set_const_values(self):
        if self._unit == "K":
            self._size = self._size * 1024
        elif self._unit == "M":
            self._size = self._size * 1024 * 1024
                
    def _set_values(self):
        for param in self._list_params:
            if type(param) is Size:
                self._size = param.get_value()
            elif type(param) is Fit:
                self._fit = param.get_value()
            elif type(param) is Unit:
                self._unit = param.get_value()
            elif type(param) is Path:
                self._path = param.get_value()
                self._file_name = param.filename
        if self._path == "":
            Functions().err_msg("MKDISK", "No se especificó el parámetro obligatorio PATH");
            return False
        if self._size == -1:
            Functions().err_msg("MKDISK", "No se especificó el parámetro obligatorio SIZE");
            return False
        if self._size < 0:
            Functions().err_msg("MKDISK", "El parámetro SIZE no puede ser negativo o cero");
            return False
        if self._unit != "K" and self._unit != "M":
            Functions().err_msg("MKDISK", "El parámetro UNIT solo puede ser K o M");
            return False
        if self._fit != "BF" and self._fit != "FF" and self._fit != "WF":
            Functions().err_msg("MKDISK", "El parámetro FIT solo puede ser BF, FF o WF");
            return False
        return True