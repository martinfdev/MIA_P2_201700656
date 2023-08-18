from src.Primitive import  *
from src.Functions import Functions as fns
from src.BinaryFileManager import BinaryFileManager as bfm
from src.UtilClass import MBR as mbr
class Mkdisk:
    def __init__(self, list_params) -> None:
        self._list_params = list_params
        self._size = -1
        self._path = ""
        self._fit = "FF"
        self._unit = "M"
        self._file_name = ""

    def execute_mkdisk(self):
        if not self._set_values():
            fns().err_msg("MKDISK", "No se pudo crear el disco "+fns().CYAN+self._file_name)
            return
        if not self._create_disk():
            fns().err_msg("MKDISK", "No se pudo crear el disco "+fns().CYAN+self._file_name)
            return
        if not self._write_mbr():
            fns().err_msg("MKDISK", "No se pudo crear el disco "+fns().CYAN+self._file_name)
            return 

    def _set_values(self):
        for param in self._list_params:
            if isinstance(param, Size):
                self._size = param.get_value()
            elif isinstance(param, Fit):
                self._fit = param.get_value()
            elif isinstance(param, Unit):
                self._unit = param.get_value()
            elif isinstance(param, Path):
                self._path = param.path
                self._file_name = param.filename

        if self._path == "":
            fns().err_msg("MKDISK", "No se especificó el parámetro obligatorio PATH");    
            return False
        else:
            function = fns()
            if not function.check_status_folder(self._path):
                function.create_folder(self._path, "MKDISK")
        if self._size == -1:
            fns().err_msg("MKDISK", "No se especificó el parámetro obligatorio SIZE");
            return False
        if self._size == None:
            fns().err_msg("MKDISK", "No se especificó el parámetro obligatorio SIZE");
            return False
        elif self._size <= 0:
            fns().err_msg("MKDISK", "El parámetro SIZE no puede ser negativo o cero");
            return False
        if self._unit != "K" and self._unit != "M":
            fns().err_msg("MKDISK", "El parámetro UNIT solo puede ser K o M");
            return False
        if self._fit != "BF" and self._fit != "FF" and self._fit != "WF":
            fns().err_msg("MKDISK", "El parámetro FIT solo puede ser BF, FF o WF");
            return False
        return True
    
    def _set_value_unit(self):
        if self._size != None:
            if self._unit == "K":
                return self._size * 1024 # 1 KB = 1024 bytes
            elif self._unit == "M":
                return self._size * 1024 * 1024 # 1 MB = 1024 KB = 1024 * 1024 bytes
            elif self._unit == "B": return self._size # bytes

    def _get_fit_for_mbr(self):
        if self._fit == "BF": return "B"
        elif self._fit == "FF": return "F"
        elif self._fit == "WF": return "W"

    def _create_disk(self):
        function = fns()
        self._size = self._set_value_unit()
        if not function.check_status_file(self._path+self._file_name):
            if not bfm(self._path+self._file_name).create_file():
                function.err_msg("MKDISK", "No se pudo crear el archivo "+function.CYAN+self._file_name)
                return False
        else:
            bfm(self._path+self._file_name).create_file() 
            function.success_msg("MKDISK", "archivo "+function.CYAN+self._file_name+function.RESET+" reescrito!")
        return bfm(self._path+self._file_name).fill_binary_file(self._size, 0)
    
    def _write_mbr(self):
        new_mbr = mbr()
        new_mbr.setValues(self._size, fns().get_time_stamp(), fns().get_random_mumber(1, 200000), self._get_fit_for_mbr())
        bfm(self._path+self._file_name).write_binary_data(new_mbr.serialize_mbr(), 0)
        return True